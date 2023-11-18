import os
import string

from avalon.data import punctuation_replacements as replacements


def is_directory(directory: str) -> bool:
    """Return True if directory passed exists on local machine,
    otherwise return False.
    """
    return os.path.isdir(directory)


def get_directory(path: str) -> str:
    """Return directory name of file path passed."""
    return os.path.dirname(path)


def get_song_file_paths(directory: str) -> list[str]:
    """Return list of music file paths in directory passed."""
    songs = os.listdir(directory)

    for song in songs.copy():
        # These are the only acceptable music file formats.
        if not song.endswith(".flac") and not song.endswith(".mp3"):
            songs.remove(song)
        else:
            songs[songs.index(song)] = os.path.join(directory, song)

    return songs


def rename_music_file(path: str, filename: str) -> str:
    """Rename local music file passed to filename passed and return
    new file path.
    """
    directory = get_directory(path)
    extension = os.path.splitext(path)[1]
    os.rename(path, f"{directory}/{filename}{extension}")

    return f"{directory}/{filename}{extension}"


def format_song_filename(title: str, number: str) -> str:
    """Format song filename for use in a file path."""
    return f"{format_track_number(number)}_{format_filename(title)}"


def format_track_number(number: str) -> str:
    """Add leading zero to single digit track numbers."""
    return f"0{number}" if int(number) < 10 else number


def format_filename(filename: str) -> str:
    """Format filename for use in a file path."""
    return replace_punctuation(filename).replace(" ", "_").lower()


def replace_punctuation(name: str) -> str:
    """Remove/replace punctuation in string passed."""
    for mark in list(string.punctuation):
        if mark in replacements.keys():
            name = name.replace(mark, replacements[mark])
        else:
            name = name.replace(mark, "")

    # Remove superfluous spaces.
    while "  " in name:
        name = name.replace("  ", " ")

    return name
