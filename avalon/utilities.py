import os

def is_directory(directory: str) -> bool:
    """Return True if directory exists on local machine, otherwise
    return False.
    """
    return os.path.isdir(directory)


def get_song_file_paths(directory: str) -> list[str]:
    """Return list of music file paths in directory."""
    songs = os.listdir(directory)

    for song in songs.copy():
        # These are the only acceptable music file formats.
        if not song.endswith(".flac") and not song.endswith(".mp3"):
            songs.remove(song)
        else:
            songs[songs.index(song)] = os.path.join(directory, song)

    return songs
