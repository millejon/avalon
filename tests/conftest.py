import pytest
import tempfile
import os

from avalon import create_app
import avalon.database as db
from avalon.data import database as db_data
import tests.data as data


@pytest.fixture
def app(tmp_path):
    # Create a temporary database for testing purposes.
    database_file, database_path = tempfile.mkstemp()

    app = create_app(
        test_config={
            "TESTING": True,
            "DATABASE": database_path,
            "MUSIC_DIRECTORY": str(tmp_path),
        }
    )

    with app.app_context():
        db.initialize_database()

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
def album_directory(tmp_path, dummy_file):
    for x in range(len(data.avalon_metadata) - 1):
        dummy_file(".flac")
    dummy_file(".mp3")
    dummy_file(".jpg")

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


@pytest.fixture
def database_album():
    def add_album_to_database(metadata: dict) -> int:
        return db.execute_write_query(
            query=db_data["albums"]["queries"]["write"],
            data=(
                metadata["album"],
                metadata["release_date"],
                metadata["multidisc"],
                metadata["single"],
            ),
        )

    return add_album_to_database


@pytest.fixture
def database_disc():
    def add_disc_to_database(metadata: dict, album: int) -> int:
        return db.execute_write_query(
            query=db_data["discs"]["queries"]["write"],
            data=(
                album,
                metadata["disc_name"],
                metadata["disc_number"],
            ),
        )

    return add_disc_to_database


@pytest.fixture
def database_song():
    def add_song_to_database(metadata: dict, album: int) -> int:
        return db.execute_write_query(
            query=db_data["songs"]["queries"]["write"],
            data=(
                album,
                None,
                metadata["title"],
                metadata["track_number"],
                metadata["length"],
                metadata["path"],
                metadata["source"],
            ),
        )

    return add_song_to_database
