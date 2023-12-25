import sqlite3

import avalon.database as db
import avalon.utilities as util
from avalon.album import Album
from avalon.song import Song
from avalon.data import database


class Artist:
    def __init__(self, id: int):
        self.id = id
        self.name = self.get_artist_name()
        self.albums = self.get_albums()
        self.songs = self.get_songs()
        self.singles = self.get_singles()
        self.produced_songs = self.get_produced_songs()
        self.photo = self.get_artist_photo()

    def get_artist_name(self) -> str:
        """Return artist name."""
        return db.execute_read_query(
            query=database["artists"]["queries"]["read"]["all"],
            data=(self.id,),
        )[0]["name"]

    def get_albums(self) -> list[Album] | None:
        """Return Album instance for all of the albums released by the
        artist.
        """
        albums = db.execute_read_query(
            query=database["artists_albums"]["queries"]["read"]["albums"],
            data=(self.id,),
        )

        return [Album(album["id"]) for album in albums] if albums else None

    def get_songs(self) -> list[Song] | None:
        """Return Song instance for all of the songs the artist is
        featured on."""
        songs = []
        artist_songs = db.execute_read_query(
            query=database["artists_songs"]["queries"]["read"]["songs"],
            data=(self.id,),
        )

        for artist_song in artist_songs:
            song = Song(artist_song["id"])
            song.album_cover = Album(song.album_id).cover
            songs.append(song)

        return songs if artist_songs else None

    def get_singles(self) -> list[Album] | None:
        """Return Album instance for all of the singles released by the
        artist.
        """
        singles = db.execute_read_query(
            query=database["artists_albums"]["queries"]["read"]["singles"],
            data=(self.id,),
        )

        return [Album(single["id"]) for single in singles] if singles else None

    def get_produced_songs(self) -> list[Song] | None:
        """Return Song instance for all of the songs the artist
        produced.
        """
        songs = []
        produced_songs = db.execute_read_query(
            query=database["producers_songs"]["queries"]["read"]["songs"],
            data=(self.id,),
        )

        for produced_song in produced_songs:
            song = Song(produced_song["id"])
            song.producer_role = self.get_producer_role(produced_song)
            song.album_cover = Album(song.album_id).cover
            songs.append(song)

        return songs if produced_songs else None

    def get_producer_role(self, song: sqlite3.Row) -> str:
        """Return type of producer the artist was credited as on a
        song.
        """
        if song["coproducer"]:
            return "Co-Producer"
        elif song["additional"]:
            return "Additional Producer"
        else:
            return "Producer"

    def get_artist_photo(self) -> str:
        """Return file path to artist profile picture."""
        if self.albums:
            return f"{util.format_directory(self.name)}/profile.jpg"
        else:
            return "default.png"
