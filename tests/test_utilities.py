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
        f"{len(music_file_paths)} music files found in {album_directory}, expected: 4"

    for file in file_paths:
        file_path = os.path.join(album_directory, file)
        if file_path.endswith(".flac") or file_path.endswith(".mp3"):
            assert file_path in music_file_paths, \
                f"get_song_file_paths() did not find {file} in {album_directory}"
        else:
            assert file_path not in music_file_paths, \
                f"get_song_file_paths() returned non-music file {file} in {album_directory}"


# rename_music_file() should rename the local file passed to the
# filename passed.
@pytest.mark.parametrize("suffix", [".flac", ".mp3"])
@pytest.mark.parametrize("filename", (
    "05_police_state",
    "this is a file",
    "16_its_bigger_than_hiphop",
))
def test_rename_music_file(suffix, filename, dummy_file):
    file_path = dummy_file(suffix)
    directory = os.path.dirname(file_path)

    util.rename_music_file(file_path, filename)

    assert not os.path.isfile(file_path), f"{file_path} still exists in {directory}"
    assert os.path.isfile(f"{directory}/{filename}{suffix}"), \
        f"{file_path} was not renamed to {filename}{suffix} in {directory}"


# format_song_filename() should format song filenames to correspond
# with the passed arguments.
@pytest.mark.parametrize(("title", "number", "filename"), (
    ("Hold On, Be Strong", "1", "01_hold_on_be_strong"),
    ("Return Of The 'G'", "2", "02_return_of_the_g"),
    ("Y'all Scared", "13", "13_yall_scared"),
))
def test_format_song_filename(title, number, filename):
    assert util.format_song_filename(title, number) == filename


# format_track_number() should add a leading zero to numbers less than
# 10.
@pytest.mark.parametrize(("number", "track_number"), (
    ("1", "01"),
    ("9", "09"),
    ("10", "10"),
    ("11", "11"),
    ("48", "48"),
))
def test_format_track_number(number, track_number):
    assert util.format_track_number(number) == track_number, \
        f"{track_number} was not formatted correctly"
    assert isinstance(util.format_track_number(number), str), \
        "format_track_number() did not return a string value"


# format_filename() should format the filename passed by removing
# punctuation and replacing spaces with underscores.
@pytest.mark.parametrize(("filename", "formatted_filename"), (
    ("THIS    IS  A   SONG TITLE", "this_is_a_song_title"),
    ("Stay Alive In N.Y.C.", "stay_alive_in_nyc"),
    ("I Don't Like To Dream About Gettin' Paid", "i_dont_like_to_dream_about_gettin_paid"),
))
def test_format_filename(filename, formatted_filename):
    assert util.format_filename(filename) == formatted_filename


# format_directory() should format the directory passed by removing
# punctuation and replacing spaces with hyphens.
@pytest.mark.parametrize(("directory", "formatted_directory"), (
    ("THIS    IS  AN    ALBUM TITLE", "this-is-an-album-title"),
    ("Enter The Wu-Tang (36 Chambers)", "enter-the-wutang-36-chambers"),
    ("Lifestylez Ov Da Poor & Dangerous", "lifestylez-ov-da-poor-and-dangerous"),
))
def test_format_directory(directory, formatted_directory):
    assert util.format_directory(directory) == formatted_directory


# replace_punctuation() should remove all punctuation from the string
# passed, except for special cases where the punctuation is replaced
# with a word.
@pytest.mark.parametrize(("name", "result"), (
    ("This    test worked!", "This test worked"),
    ("!\"#$   %&'()*+,-.  /:;<=>?@[\\]^_`{|}~", "number andand equals"),
    ("Wu-Tang: 7th Chamber, Pt. II", "WuTang 7th Chamber Pt II"),
))
def test_replace_punctuation(name, result):
    assert util.replace_punctuation(name) == result
