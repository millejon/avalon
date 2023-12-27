import avalon.database as db
import avalon.utilities as util
from avalon.album import Album
from avalon.song import Song
from avalon.data import database


class Hub:
    def __init__(self, id: int):
        self.id = id
        self.name = self.get_hub_name()
        self.albums = self.get_albums()
        self.songs = self.get_songs()
        self.photo = self.get_hub_photo()

    def get_hub_name(self) -> str:
        """Return hub name."""
        return db.execute_read_query(
            query=database["hubs"]["queries"]["read"]["all"],
            data=(self.id,),
        )[0]["name"]

    def get_albums(self) -> list[Album] | None:
        """Return Album instance for all of the albums related to the hub."""
        albums = db.execute_read_query(
            query=database["hubs_albums"]["queries"]["read"]["all"],
            data=(self.id,),
        )

        return [Album(album["album_id"]) for album in albums] if albums else None

    def get_songs(self) -> list[Song] | None:
        """Return Song instance for all of the songs related to the hub."""
        songs = []
        hub_songs = db.execute_read_query(
            query=database["hubs_albums"]["queries"]["read"]["songs"],
            data=(self.id,),
        )

        for hub_song in hub_songs:
            song = Song(hub_song["id"])
            song.album_cover = Album(song.album_id).cover
            songs.append(song)

        return songs if hub_songs else None

    def get_hub_photo(self) -> str:
        """Return file path to hub profile picture."""
        return f"{util.format_directory(self.name)}/profile.jpg"
