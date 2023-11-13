import pytest

import avalon.metadata_tagger as tagger
from avalon.data import required_metadata_input_fields as form_fields
from tests.data import metadata_form


# Submitting a valid directory to the input-metadata route should
# display the form to input metadata.
def test_input_metadata(client, album_directory):
    assert client.get("/metadata-tagger/input-metadata").status_code == 200
    response = client.post("/metadata-tagger/input-metadata",
                           data={"directory": album_directory})
    assert response.status_code == 200
    assert b'<label for="album_artists">' in response.data


# Submitting a local directory that does not contain any music files to
# the input-metadata route should alert the user of the error and
# reload the page.
def test_input_metadata_empty_directory(client, tmp_path):
    response = client.post("/metadata-tagger/input-metadata",
                           data={"directory": tmp_path})
    assert b"No music files in directory!" in response.data
    assert response.status_code == 200


# Submitting a directory that does not exist locally to the
# input-metadata route should alert the user of the error and reload
# the page.
def test_input_metadata_invalid_directory(client):
    response = client.post("/metadata-tagger/input-metadata",
                           data={"directory": "not/a/directory"})
    assert b"Directory does not exist!" in response.data
    assert response.status_code == 200


fields = (form_fields["album"] + form_fields["multidisc"]
          + [f"track1_{field}" for field in form_fields["song"]])
fields.append(f"track1_producers")


# Submitting a metadata form that is missing one of the required fields
# should raise an exception that specifies what field is missing.
@pytest.mark.parametrize("field", fields)
def test_validate_metadata_form_missing_required_fields(field):
    metadata = metadata_form.copy()
    metadata[field] = ""

    with pytest.raises(ExceptionGroup) as error:
        tagger.validate_metadata_form(metadata)

    assert f"Value for '{field}' is missing!" == str(error.value.exceptions[0])
    

# Submitting a metadata form that has both single and multidisc flags
# set should raise an exception.
def test_validate_metadata_form_single_multidisc():
    metadata = metadata_form.copy()
    metadata["single"] = "True"

    with pytest.raises(ExceptionGroup) as error:
        tagger.validate_metadata_form(metadata)

    assert f"An album can not be a single and multidisc!" == str(error.value.exceptions[0])


# Submitting a metadata form with complete multidisc metadata but
# without the multidisc flag set should raise an exception.
def test_validate_metadata_form_missing_multidisc_flag():
    metadata = metadata_form.copy()
    metadata.pop("multidisc")

    with pytest.raises(ExceptionGroup) as error:
        tagger.validate_metadata_form(metadata)

    assert f"Value for 'multidisc' is missing!" == str(error.value.exceptions[0])


fields = form_fields["multidisc"].copy()


# Submitting a metadata form with incomplete multidisc metadata and
# without the multidisc flag set should raise an exception about setting
# the multidisc flag and an exception that specifies what field is
# missing.
@pytest.mark.parametrize("field", fields)
def test_validate_metadata_form_incomplete_multidisc(field):
    metadata = metadata_form.copy()
    metadata.pop("multidisc")
    metadata[field] = ""

    with pytest.raises(ExceptionGroup) as error:
        tagger.validate_metadata_form(metadata)

    assert f"Value for 'multidisc' is missing!" == str(error.value.exceptions[0])
    assert f"Value for '{field}' is missing!" == str(error.value.exceptions[1])
