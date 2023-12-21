import sqlite3

import avalon.database as db
from avalon.song import Song
from avalon.data import database


class Album:
    def __init__(self, id: int):
        self.id = id

    def get_album_info(self) -> None:
        """Populate class properties with album data retrieved from
        database.
        """
        info = db.execute_read_query(
            query=database["albums"]["queries"]["read"]["all"],
            data=(self.id,),
        )[0]

        self.name = info["name"]
        self.release_date = info["release_date"]
        self.multidisc = True if info["multidisc"] else False

    def get_album_artists(self) -> list[sqlite3.Row]:
        """Return database id and artist name for all of the artists
        the album was released under.
        """
        return db.execute_read_query(
            query=database["artists_albums"]["queries"]["read"]["artists"],
            data=(self.id,),
        )

    def get_songs(self) -> list[Song]:
        """Return Song instance for all of the songs on the album."""
        songs = db.execute_read_query(
            query=database["songs"]["queries"]["read"]["album"],
            data=(self.id,),
        )
        self.song_count = len(songs)

        return [Song(song["id"]) for song in songs]

    def get_length(self) -> str:
        """Return total length of all songs on the album."""
        length = round(
            db.execute_read_query(
                query=database["albums"]["queries"]["read"]["length"],
                data=(self.id,),
            )[0][0]
        )

        hours, remainder = divmod(length, 3600)
        minutes, seconds = divmod(remainder, 60)

        if length >= 3600:
            return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        else:
            return "{:d}:{:02d}".format(minutes, seconds)
