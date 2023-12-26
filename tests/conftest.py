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
    database, database_path = tempfile.mkstemp()

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
    os.close(database)
    os.unlink(database_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def dummy_album_directory(tmp_path, dummy_file):
    for _ in range(len(data.avalon_metadata) - 1):
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
            query=db_data["albums"]["queries"]["write"]["add"],
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
            query=db_data["discs"]["queries"]["write"]["add"],
            data=(
                album,
                metadata["disc_title"],
                metadata["disc_number"],
            ),
        )

    return add_disc_to_database


@pytest.fixture
def database_song():
    def add_song_to_database(metadata: dict, album: int, disc: int = None) -> int:
        return db.execute_write_query(
            query=db_data["songs"]["queries"]["write"]["add"],
            data=(
                album,
                disc,
                metadata["title"],
                metadata["track_number"],
                metadata["length"],
                metadata["path"],
                metadata["source"],
            ),
        )

    return add_song_to_database


@pytest.fixture
def artist_count():
    artists = []

    for song in data.avalon_metadata:
        artists.extend(song["album_artists"])
        artists.extend(song["song_artists"])

        if "group_members" in song.keys():
            artists.extend(song["group_members"])
        if "producers" in song.keys():
            artists.extend(song["producers"])
        if "coproducers" in song.keys():
            artists.extend(song["coproducers"])
        if "additional_producers" in song.keys():
            artists.extend(song["additional_producers"])

    return len(set(artists))


@pytest.fixture
def album_count():
    return len(set([song["album"] for song in data.avalon_metadata]))


@pytest.fixture
def song_count():
    return len(set([tuple(song) for song in data.avalon_metadata]))


@pytest.fixture
def hub_count():
    hubs = []

    for song in data.avalon_metadata:
        if "hubs" in song.keys():
            hubs.extend(song["hubs"])

    return len(set(hubs))
