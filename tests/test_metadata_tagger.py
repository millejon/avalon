from flask import session


# Submitting a valid directory to the input-metadata route should
# display the form to input metadata.
def test_input_metadata_valid_directory(client, album_directory):
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
