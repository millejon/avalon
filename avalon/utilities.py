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
    files = os.listdir(directory)

    for file in files.copy():
        # These are the only acceptable music file formats.
        if not file.endswith(".flac") and not file.endswith(".mp3"):
            files.remove(file)

    return [os.path.join(directory, song) for song in files]


def rename_music_file(current_file_path: str, filename: str) -> str:
    """Rename local music file passed to filename passed and return
    new file path.
    """
    directory = get_directory(current_file_path)
    extension = os.path.splitext(current_file_path)[1]
    new_file_path = f"{directory}/{filename}{extension}"
    os.rename(current_file_path, new_file_path)

    return new_file_path


def format_song_filename(number: str, title: str) -> str:
    """Format song filename for use in a file path."""
    return f"{format_track_number(number)}_{format_filename(title)}"


def format_track_number(number: str) -> str:
    """Add leading zero to single digit track numbers."""
    return f"0{number}" if int(number) < 10 else number


def format_filename(filename: str) -> str:
    """Format filename for use in a file path."""
    return replace_punctuation(filename).replace(" ", "_").lower()


def format_directory(directory: str) -> str:
    """Format directory filename for use in a file path."""
    return replace_punctuation(directory).replace(" ", "-").lower()


def replace_punctuation(text: str) -> str:
    """Remove/replace punctuation in string passed."""
    for mark in list(string.punctuation):
        if mark in replacements.keys():
            text = text.replace(mark, replacements[mark])
        else:
            text = text.replace(mark, "")

    # Remove superfluous spaces.
    while "  " in text:
        text = text.replace("  ", " ")

    return text


def format_song_file_path(metadata: dict) -> str:
    """Format file path for song to correspond with its metadata."""
    artist = format_directory(metadata["album_artists"][0])
    album = format_directory(metadata["album"])
    song = format_song_filename(metadata["track_number"], metadata["title"])

    return f"{artist}/{album}/{song}.flac"
