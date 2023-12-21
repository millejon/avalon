from avalon.update_database import update_database
from avalon.metadata_tagger import process_songs
import avalon.database as db
import avalon.utilities as util
import tests.data as data


def test_update_database(
    app, dummy_album_directory, artist_count, album_count, song_count, hub_count
):
    with app.app_context():
        files = util.get_song_file_paths(dummy_album_directory)
        metadata = data.song_metadata.copy()

        for index, file in enumerate(files):
            metadata[index]["path"] = file

        process_songs(metadata)
        update_database()

        assert len(db.execute_read_query("""SELECT * FROM artists""")) == artist_count
        assert len(db.execute_read_query("""SELECT * FROM albums""")) == album_count
        assert len(db.execute_read_query("""SELECT * FROM songs""")) == song_count
        assert len(db.execute_read_query("""SELECT * FROM hubs""")) == hub_count
