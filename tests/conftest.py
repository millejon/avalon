import pytest
import tempfile
import os

from avalon import create_app
from avalon.database import initialize_database
import tests.data as data


@pytest.fixture
def app(tmp_path):
    # Create a temporary database for testing purposes.
    database_file, database_path = tempfile.mkstemp()

    app = create_app(
        test_config={
            "TESTING": True,
            "DATABASE": database_path,
            "MUSIC_DIRECTORY": tmp_path,
        }
    )

    with app.app_context():
        initialize_database()

    yield app

    # Close and delete temporary database.
    os.close(database_file)
    os.unlink(database_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def album_directory(tmp_path):
    for x in range(3):
        tempfile.mkstemp(suffix=".flac", dir=tmp_path)
    tempfile.mkstemp(suffix=".mp3", dir=tmp_path)
    tempfile.mkstemp(suffix=".jpg", dir=tmp_path)
    tempfile.mkstemp(suffix=".txt", dir=tmp_path)

    return tmp_path


@pytest.fixture
def dummy_file(tmp_path):
    def create_dummy_file(suffix: str) -> str:
        file, file_path = tempfile.mkstemp(suffix=suffix, dir=tmp_path)
        with open(file_path, "bw") as dummy_file:
            dummy_file.write(data.dummy_files[suffix])
        os.close(file)

        if suffix == ".jpg":
            os.rename(file_path, f"{tmp_path}/cover.jpg")

        return file_path

    return create_dummy_file
