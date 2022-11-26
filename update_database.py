import os
import db_operations as db
from extract_song_data import Song

MUSIC_DIRECTORY = "D:\\Music"
EXTENSIONS = ('.flac', '.mp3')

for root, dirs, files in os.walk(MUSIC_DIRECTORY):
    if root[0:21] == "D:\\Music\\_in_progress":
        continue

    for file in files:
        file_extension = os.path.splitext(file)[1]
        if file_extension not in EXTENSIONS:
            continue

        song_path = os.path.join(root, file)

        # Skip song if it is already in database.
        song_id = db.get_song_id(song_path)
        if song_id is not None:
            continue

        song = Song(song_path)

        album_artists = db.add_artists(song.album_artists)
        album_id = db.add_album(song)
        db.add_artist_album_link(album_artists, album_id)

        if song.multi_disc is True:
            disc_id = db.add_disc(album_id, song)
        else:
            disc_id = None

        song_id = db.add_song(song, album_id, disc_id)

        song_artists = db.add_artists(song.song_artists)
        db.add_artist_song_link(song_artists, song_id, 0)

        if song.group_members is not None:
            group_members = db.add_artists(song.group_members)
            db.add_artist_song_link(group_members, song_id, 1)
