from datetime import datetime
import sqlite3

import avalon.database as db
from avalon.data import database


class Song:
    def __init__(self, id: int):
        self.id = id

    def get_song_info(self) -> None:
        """Populate class properties with song data retrieved from
        database.
        """
        info = db.execute_read_query(
            query=database["songs"]["queries"]["read"]["all"],
            data=(self.id,),
        )[0]

        self.name = info["name"]
        self.track_number = info["track_number"]
        self.length = datetime.fromtimestamp(round(info["length"])).strftime("%#M:%S")
        self.path = info["path"]
        self.album_id = info["album_id"]

    def get_song_artists(self) -> list[sqlite3.Row]:
        """Return database id and artist name for all of the artists
        featured on the song.
        """
        return db.execute_read_query(
            query=database["artists_songs"]["queries"]["read"]["artists"],
            data=(self.id,),
        )

    def get_album_name(self) -> str:
        """Return name of album the song appears on."""
        return db.execute_read_query(
            query=database["albums"]["queries"]["read"]["all"],
            data=(self.album_id,),
        )[0]["name"]

    def get_producers(self) -> list[sqlite3.Row]:
        """Return database id and producer name for all of the main
        producers of the song.
        """
        return db.execute_read_query(
            query=database["producers_songs"]["queries"]["read"]["producers"],
            data=(self.id,),
        )
