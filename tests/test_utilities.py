import pytest
import os

import avalon.utilities as util


# is_directory() should return True when passed a path to a local
# directory.
def test_is_directory(tmp_path):
    assert util.is_directory(tmp_path)


# is_directory() should return False when passed a path to a directory
# that does not exist locally.
def test_is_not_directory():
    directory = "this/is/not/a/directory"
    assert not util.is_directory(directory)


# get_song_file_paths() should return an empty list when passed an empty
# directory.
def test_get_song_file_paths_empty_directory(tmp_path):
    file_paths = util.get_song_file_paths(directory=tmp_path)
    assert file_paths == []


# get_directory() should return the directory name of the file path
# passed.
@pytest.mark.parametrize(("path, directory"), (
    ("C:/music/artist/album/01_track1.flac", "C:/music/artist/album"),
    ("02_track2.flac", ""),
    ("artist/album/03_track3.mp3", "artist/album"),
))
def test_get_directory(path, directory):
    assert util.get_directory(path) == directory


# get_song_file_paths() should return a list of file paths for only the
# music files in the directory passed.
def test_get_song_file_paths(album_directory):
    file_paths = os.listdir(album_directory)
    music_file_paths = util.get_song_file_paths(directory=album_directory)

    assert len(music_file_paths) == 4, \
        f"{len(music_file_paths)} music files found in {album_directory}, expected: 4."

    for file in file_paths:
        file_path = os.path.join(album_directory, file)
        if file_path.endswith(".flac") or file_path.endswith(".mp3"):
            assert file_path in music_file_paths, \
                f"get_song_file_paths() did not find {file} in {album_directory}."
        else:
            assert file_path not in music_file_paths, \
                f"get_song_file_paths() returned non-music file {file} in {album_directory}."
