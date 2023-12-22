from datetime import datetime
import sqlite3

import avalon.database as db
from avalon.data import database


class Song:
    def __init__(self, id: int):
        self.id = id
        self.title = None
        self.track_number = None
        self.length = None
        self.path = None
        self.album_id = None
        self.album = None
        self.album_cover = None  # Value assigned in Artist class.
        self.producer_role = None  # Value assigned in Artist class.
        self.populate_song_info()
        self.song_artists = self.get_song_artists()
        self.producers = self.get_producers()

    def populate_song_info(self) -> None:
        """Populate class properties with song data retrieved from
        database.
        """
        info = db.execute_read_query(
            query=database["songs"]["queries"]["read"]["all"],
            data=(self.id,),
        )[0]

        self.title = info["title"]
        self.track_number = info["track_number"]
        self.length = datetime.fromtimestamp(round(info["length"])).strftime("%#M:%S")
        self.path = info["path"]
        self.album_id = info["album_id"]
        self.album = self.get_album_title()

    def get_album_title(self) -> str:
        """Return title of album the song appears on."""
        return db.execute_read_query(
            query=database["albums"]["queries"]["read"]["all"],
            data=(self.album_id,),
        )[0]["title"]

    def get_song_artists(self) -> list[sqlite3.Row]:
        """Return database id and artist name for all of the artists
        featured on the song.
        """
        return db.execute_read_query(
            query=database["artists_songs"]["queries"]["read"]["artists"],
            data=(self.id,),
        )

    def get_producers(self) -> list[sqlite3.Row]:
        """Return database id and producer name for all of the main
        producers of the song.
        """
        return db.execute_read_query(
            query=database["producers_songs"]["queries"]["read"]["producers"],
            data=(self.id,),
        )
