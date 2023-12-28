import sqlite3

import avalon.database as db
import avalon.utilities as util
from avalon.song import Song
from avalon.data import database


class Album:
    def __init__(self, id: int):
        self.id = id
        self.title = None
        self.release_date = None
        self.multidisc = None
        self.populate_album_info()
        self.album_artists = self.get_album_artists()
        self.cover = self.get_album_cover()
        self.songs = None
        self.song_count = 0
        self.length = None

    def populate_album_info(self) -> None:
        """Populate class properties with album data retrieved from
        database.
        """
        info = db.execute_read_query(
            query=database["albums"]["queries"]["read"]["all"],
            data=(self.id,),
        )[0]

        self.title = info["title"]
        self.release_date = info["release_date"]
        self.multidisc = True if info["multidisc"] else False

    def populate_tracklist(self) -> None:
        """Populate class properties related to album tracklist."""
        self.songs = self.get_songs()
        self.song_count = len(self.songs)
        self.length = self.get_album_length()

    def get_album_artists(self) -> list[sqlite3.Row]:
        """Return database id and artist name for all of the artists
        the album was released under.
        """
        return db.execute_read_query(
            query=database["artists_albums"]["queries"]["read"]["artists"],
            data=(self.id,),
        )

    def get_songs(self) -> None:
        """Return Song instance for all of the songs on the album."""
        songs = db.execute_read_query(
            query=database["songs"]["queries"]["read"]["album"],
            data=(self.id,),
        )

        return [Song(song["id"]) for song in songs]

    def get_album_length(self) -> str:
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

    def get_album_cover(self) -> str:
        """Return file path to album cover."""
        artist = util.format_directory(self.album_artists[0]["name"])
        album = util.format_directory(self.title)

        return f"{artist}/{album}/cover.jpg"
