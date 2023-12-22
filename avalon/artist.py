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

    def get_albums(self) -> list[Album]:
        """Return Album instance for all of the albums released by the
        artist.
        """
        albums = db.execute_read_query(
            query=database["artists_albums"]["queries"]["read"]["albums"],
            data=(self.id,),
        )

        return [Album(album["id"]) for album in albums] if albums else None

    def get_songs(self) -> list[Song]:
        """Return Song instance for all of the songs the artist is
        featured on."""
        songs = db.execute_read_query(
            query=database["artists_songs"]["queries"]["read"]["songs"],
            data=(self.id,),
        )

        return [Song(song["id"]) for song in songs] if songs else None

    def get_singles(self) -> list[Album]:
        """Return Album instance for all of the singles released by the
        artist.
        """
        singles = db.execute_read_query(
            query=database["artists_albums"]["queries"]["read"]["singles"],
            data=(self.id,),
        )

        return [Album(single["id"]) for single in singles] if singles else None

    def get_produced_songs(self) -> list[Song]:
        """Return Song instance for all of the songs the artist
        produced.
        """
        songs = db.execute_read_query(
            query=database["producers_songs"]["queries"]["read"]["songs"],
            data=(self.id,),
        )

        produced_songs = [Song(song["id"]) for song in songs] if songs else None

        if produced_songs:
            for index, song in enumerate(produced_songs):
                if songs[index]["coproducer"]:
                    song.producer_role = "Co-Producer"
                elif songs[index]["additional"]:
                    song.producer_role = "Additional Producer"
                else:
                    song.producer_role = "Producer"

        return produced_songs

    def get_artist_photo(self) -> str:
        """Return file path to artist profile picture."""
        if self.albums:
            return f"{util.format_directory(self.name)}/profile.jpg"
        else:
            return "default.jpg"
