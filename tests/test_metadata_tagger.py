import pytest
import os
from mutagen import File as MutagenFile

import avalon.metadata_tagger as tagger
from avalon.data import required_metadata_input_fields as required_fields
import tests.data as data


# Submitting a valid directory to the input-metadata route should
# display the form to input metadata.
def test_input_metadata(client, album_directory):
    assert client.get("/input-metadata").status_code == 200

    response = client.post("/input-metadata", data={"directory": album_directory})

    assert response.status_code == 200
    assert b'<label for="album_artists">' in response.data


# Submitting a local directory that does not contain any music files to
# the input-metadata route should alert the user of the error and
# reload the page.
def test_input_metadata_empty_directory(client, tmp_path):
    response = client.post("/input-metadata", data={"directory": tmp_path})

    assert b"No music files in directory!" in response.data
    assert response.status_code == 200


# Submitting a directory that does not exist locally to the
# input-metadata route should alert the user of the error and reload
# the page.
def test_input_metadata_invalid_directory(client):
    response = client.post("/input-metadata", data={"directory": "not/a/directory"})

    assert b"Directory does not exist!" in response.data
    assert response.status_code == 200


fields = (
    required_fields["album"]
    + required_fields["multidisc"]
    + [f"track1_{field}" for field in required_fields["song"]]
)
fields.append("track1_producers")


# Submitting a metadata form that is missing one of the required fields
# should raise an exception that specifies what field is missing.
@pytest.mark.parametrize("field", fields)
def test_validate_metadata_form_missing_required_fields(field):
    metadata = data.metadata_form.copy()
    metadata[field] = ""

    with pytest.raises(ExceptionGroup) as error:
        tagger.validate_metadata_form(metadata)

    assert f"Value for '{field}' is missing!" == str(error.value.exceptions[0])


# Submitting a metadata form that has both single and multidisc flags
# set should raise an exception.
def test_validate_metadata_form_single_multidisc():
    metadata = data.metadata_form.copy()
    metadata["single"] = "True"

    with pytest.raises(ExceptionGroup) as error:
        tagger.validate_metadata_form(metadata)

    assert "An album can not be a single and multidisc!" == str(
        error.value.exceptions[0]
    )


# Submitting a metadata form with complete multidisc metadata but
# without the multidisc flag set should raise an exception.
def test_validate_metadata_form_missing_multidisc_flag():
    metadata = data.metadata_form.copy()
    metadata.pop("multidisc")

    with pytest.raises(ExceptionGroup) as error:
        tagger.validate_metadata_form(metadata)

    assert "Value for 'multidisc' is missing!" == str(error.value.exceptions[0])


# Submitting a metadata form with incomplete multidisc metadata and
# without the multidisc flag set should raise an exception about setting
# the multidisc flag and an exception that specifies what field is
# missing.
@pytest.mark.parametrize("field", required_fields["multidisc"])
def test_validate_metadata_form_incomplete_multidisc(field):
    metadata = data.metadata_form.copy()
    metadata.pop("multidisc")
    metadata[field] = ""

    with pytest.raises(ExceptionGroup) as error:
        tagger.validate_metadata_form(metadata)

    assert "Value for 'multidisc' is missing!" == str(error.value.exceptions[0])
    assert f"Value for '{field}' is missing!" == str(error.value.exceptions[1])


# format_metadata() should return a list of dictionaries containing the
# formatted metadata.
def test_format_metadata():
    metadata = tagger.format_metadata(data.metadata_form.copy())

    assert len(metadata) == int(data.metadata_form["track_count"])

    for index, song in enumerate(metadata):
        assert song.keys() == data.formatted_metadata[index].keys()

        for key, value in data.formatted_metadata[index].items():
            assert song[key] == value


# process_songs() should add metadata to all music files and rename
# the files to correspond with their respective metadata.
def test_process_songs(dummy_file):
    metadata = data.formatted_metadata.copy()
    file_paths = [dummy_file(".flac") * len(metadata)]
    dummy_file(".jpg")
    new_file_paths = [metadata[x]["path"] for x in range(len(metadata))]

    for x in range(len(metadata)):
        metadata[x]["path"] = file_paths[x]

    tagger.process_songs(metadata)

    for x in range(len(metadata)):
        file_path = f"{os.path.dirname(file_paths[0])}/{new_file_paths[x]}"

        assert not os.path.isfile(file_paths[x])
        assert os.path.isfile(file_path)

        song = MutagenFile(file_path)

        for key, value in metadata[x].items():
            assert song[key][0] == value
