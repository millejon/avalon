import os
from flask import current_app

import avalon.database as db
from avalon.album import Album
from avalon.song import Song
from avalon.data import database


class Playlist:
    def __init__(self, id: int):
        self.id = id
        self.title = self.get_playlist_title()
        self.songs = self.get_songs()

    def get_playlist_title(self) -> str:
        """Return playlist title."""
        return db.execute_read_query(
            query=database["playlists"]["queries"]["read"]["all"],
            data=(self.id,),
        )[0]["title"]

    def get_songs(self) -> list[Song] | None:
        """Return Song instance for all of the songs in the playlist."""
        songs = []
        playlist_songs = db.execute_read_query(
            query=database["playlists_songs"]["queries"]["read"]["songs"],
            data=(self.id,),
        )

        for playlist_song in playlist_songs:
            song = Song(playlist_song["id"])
            song.album_cover = Album(song.album_id).cover
            songs.append(song)

        return songs if playlist_songs else None

    def add_song(self, song_id: int) -> None:
        """Add song to playlist."""
        db.execute_write_query(
            query=database["playlists_songs"]["queries"]["write"]["add"],
            data=(self.id, song_id),
        )

    def delete_song(self, song_id: int) -> None:
        """Remove song from playlist."""
        db.execute_write_query(
            query=database["playlists_songs"]["queries"]["write"]["delete"],
            data=(self.id, song_id),
        )

    @staticmethod
    def download_playlist(songs: list[Song]) -> None:
        """Export playlist as an M3U file."""
        music_directory = current_app.config["MUSIC_DIRECTORY"]
        with open("avalon/static/playlist.m3u", "w") as playlist:
            for song in songs:
                song_path = os.path.join(music_directory, song.path)
                playlist.write(f"{song_path}\n")
