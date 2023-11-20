import avalon.database as db
from avalon.data import database


class MetadataMapper:
    def __init__(self, metadata: dict):
        self.metadata = metadata
        self.album = self.get_album()
        self.disc = None
        self.song = None

    def get_song(self) -> int | None:
        """Return database id of a song or None if the song is not in
        the database.
        """
        song = db.execute_read_query(
            query=database["songs"]["queries"]["read"]["id"],
            data=(self.metadata["path"],),
        )

        return song[0]["id"] if song else None

    def get_album(self) -> int | None:
        """Return database id of an album or None if the album is not in
        the database.
        """
        album = db.execute_read_query(
            query=database["albums"]["queries"]["read"]["id"],
            data=(self.metadata["album"], self.metadata["release_date"]),
        )

        return album[0]["id"] if album else None

    def get_hub(self, name: str) -> int | None:
        """Return database id of a hub or None if the hub is not in the
        database."""
        hub = db.execute_read_query(
            query=database["hubs"]["queries"]["read"]["id"], data=(name,)
        )

        return hub[0]["id"] if hub else None

    def get_disc(self) -> int | None:
        """Return database id of a disc or None if the disc is not in
        the database.
        """
        disc = db.execute_read_query(
            query=database["discs"]["queries"]["read"]["id"],
            data=(self.album, self.metadata["disc_number"]),
        )

        return disc[0]["id"] if disc else None

    def get_artist(self, name: str) -> int | None:
        """Return database id of an artist or None if the artist is not
        in the database.
        """
        artist = db.execute_read_query(
            query=database["artists"]["queries"]["read"]["id"], data=(name,)
        )

        return artist[0]["id"] if artist else None

    def add_album(self) -> None:
        """Add album metadata to database."""
        if not self.album:
            self.album = db.execute_write_query(
                query=database["albums"]["queries"]["write"],
                data=(
                    self.metadata["album"],
                    self.metadata["release_date"],
                    self.metadata["multidisc"],
                    self.metadata["single"],
                ),
            )
            self.add_album_artists()

            if "hubs" in self.metadata.keys():
                self.add_hubs()

        if self.metadata["multidisc"]:
            self.disc = self.get_disc()

            if not self.disc:
                self.add_disc()

    def add_disc(self) -> None:
        """Add individual disc metadata of multi-disc album to
        database.
        """
        self.disc = db.execute_write_query(
            query=database["discs"]["queries"]["write"],
            data=(
                self.album,
                self.metadata["disc_name"],
                self.metadata["disc_number"],
            ),
        )

    def add_artists(self, artists: list[str]) -> list[int]:
        """Add artist metadata to database and return database ids of
        artists.
        """
        artist_ids = []

        for artist in artists:
            artist_id = self.get_artist(artist)

            if not artist_id:
                artist_id = db.execute_write_query(
                    query=database["artists"]["queries"]["write"], data=(artist,)
                )

            artist_ids.append(artist_id)

        return artist_ids

    def add_album_artists(self) -> None:
        """Add album artists to database and link artists to album in
        database.
        """
        for artist in self.add_artists(self.metadata["album_artists"]):
            print(artist)
            db.execute_write_query(
                query=database["artists_albums"]["queries"]["write"],
                data=(artist, self.album),
            )

    def add_song(self) -> None:
        """Add song metadata to database."""
        self.song = db.execute_write_query(
            query=database["songs"]["queries"]["write"],
            data=(
                self.album,
                self.disc,
                self.metadata["title"],
                self.metadata["track_number"],
                self.metadata["length"],
                self.metadata["path"],
                self.metadata["source"],
            ),
        )

    def add_song_artists(self) -> None:
        """Add song artists to database and link artists to song in
        database.
        """
        for artist in self.add_artists(self.metadata["song_artists"]):
            db.execute_write_query(
                query=database["artists_songs"]["queries"]["write"],
                data=(artist, self.song, False),
            )

        if "group_members" in self.metadata.keys():
            for artist in self.add_artists(self.metadata["group_members"]):
                db.execute_write_query(
                    query=database["artists_songs"]["queries"]["write"],
                    data=(artist, self.song, True),
                )

    def add_producers(self) -> None:
        """Add producers to database and link producers to song in
        database.
        """
        for producer in self.add_artists(self.metadata["producers"]):
            db.execute_write_query(
                query=database["producers_songs"]["queries"]["write"],
                data=(producer, self.song, False, False),
            )

        if "coproducers" in self.metadata.keys():
            for producer in self.add_artists(self.metadata["coproducers"]):
                db.execute_write_query(
                    query=database["producers_songs"]["queries"]["write"],
                    data=(producer, self.song, True, False),
                )

        if "additional_producers" in self.metadata.keys():
            for producer in self.add_artists(self.metadata["additional_producers"]):
                db.execute_write_query(
                    query=database["producers_songs"]["queries"]["write"],
                    data=(producer, self.song, False, True),
                )

    def add_hubs(self) -> None:
        """Add hubs to database and link album to hubs in database."""
        for hub in self.metadata["hubs"]:
            hub_id = self.get_hub(hub)

            if not hub_id:
                hub_id = db.execute_write_query(
                    query=database["hubs"]["queries"]["write"], data=(hub,)
                )

            db.execute_write_query(
                query=database["hubs_albums"]["queries"]["write"],
                data=(hub_id, self.album),
            )
