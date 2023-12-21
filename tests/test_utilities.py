import pytest
import os

import avalon.utilities as util
import tests.data as data


# is_directory() should return True when passed a path to a local
# directory.
def test_is_directory(tmp_path):
    assert util.is_directory(tmp_path)


# is_directory() should return False when passed a path to a directory
# that does not exist locally.
def test_is_not_directory():
    assert not util.is_directory("this/is/not/a/directory")


# get_directory() should return the directory name of the file path
# passed.
@pytest.mark.parametrize(
    ("path, directory"),
    (
        ("C:/music/artist/album/01_track1.flac", "C:/music/artist/album"),
        ("02_track2.flac", ""),
        ("artist/album/03_track3.mp3", "artist/album"),
    ),
)
def test_get_directory(path, directory):
    assert util.get_directory(path) == directory


# get_song_file_paths() should return an empty list when passed an empty
# directory.
def test_get_song_file_paths_empty_directory(tmp_path):
    file_paths = util.get_song_file_paths(directory=tmp_path)

    assert file_paths == []


# get_song_file_paths() should return a list of file paths for only the
# music files in the directory passed.
def test_get_song_file_paths(dummy_album_directory):
    file_paths = os.listdir(dummy_album_directory)
    music_file_paths = util.get_song_file_paths(dummy_album_directory)

    assert len(music_file_paths) == len(data.avalon_metadata)

    for file in file_paths:
        file_path = os.path.join(dummy_album_directory, file)

        if file_path.endswith(".flac") or file_path.endswith(".mp3"):
            assert file_path in music_file_paths
        else:
            assert file_path not in music_file_paths


# rename_music_file() should rename the local file passed to the
# filename passed.
@pytest.mark.parametrize("suffix", (".flac", ".mp3"))
@pytest.mark.parametrize(
    "filename",
    (
        "05_police_state",
        "this is a file",
        "16_its_bigger_than_hiphop",
    ),
)
def test_rename_music_file(dummy_file, suffix, filename):
    file_path = dummy_file(suffix)
    renamed_file = util.rename_music_file(file_path, filename)

    assert not os.path.isfile(file_path)
    assert os.path.isfile(renamed_file)


# format_song_filename() should format song filenames to correspond
# with the passed arguments.
@pytest.mark.parametrize(
    ("number", "title", "formatted"),
    (
        ("1", "Hold On, Be Strong", "01_hold_on_be_strong"),
        ("2", "Return Of The 'G'", "02_return_of_the_g"),
        ("13", "Y'all Scared", "13_yall_scared"),
    ),
)
def test_format_song_filename(number, title, formatted):
    assert util.format_song_filename(number, title) == formatted


# format_track_number() should add a leading zero to numbers less than
# 10.
@pytest.mark.parametrize(
    ("number", "track_number"),
    (
        ("1", "01"),
        ("9", "09"),
        ("10", "10"),
        ("11", "11"),
        ("48", "48"),
    ),
)
def test_format_track_number(number, track_number):
    assert util.format_track_number(number) == track_number


# format_filename() should format the filename passed by removing
# punctuation and replacing spaces with underscores.
@pytest.mark.parametrize(
    ("raw", "formatted"),
    (
        ("THIS    IS  A   SONG TITLE", "this_is_a_song_title"),
        ("Stay Alive In N.Y.C.", "stay_alive_in_nyc"),
        (
            "I Don't Like To Dream About Gettin' Paid",
            "i_dont_like_to_dream_about_gettin_paid",
        ),
    ),
)
def test_format_filename(raw, formatted):
    assert util.format_filename(raw) == formatted


# format_directory() should format the directory passed by removing
# punctuation and replacing spaces with hyphens.
@pytest.mark.parametrize(
    ("raw", "formatted"),
    (
        ("Benny The Butcher", "benny-the-butcher"),
        ("Mr. Ten08", "mr-ten08"),
        ("Balance & Options", "balance-and-options"),
    ),
)
def test_format_directory(raw, formatted):
    assert util.format_directory(raw) == formatted


# replace_punctuation() should remove all punctuation from the string
# passed, except for special cases where the punctuation is replaced
# with a word.
@pytest.mark.parametrize(
    ("raw", "formatted"),
    (
        ("This    test worked!", "This test worked"),
        ("!\"#$   %&'()*+,-.  /:;<=>?@[\\]^_`{|}~", "number andand equals"),
        ("Wu-Tang: 7th Chamber, Pt. II", "WuTang 7th Chamber Pt II"),
    ),
)
def test_replace_punctuation(raw, formatted):
    assert util.replace_punctuation(raw) == formatted


# format_song_file_path() should format the file path to a local music
# file to correspond with its metadata.
@pytest.mark.parametrize(
    ("metadata", "file_path"),
    (
        (data.avalon_metadata[0], data.avalon_metadata_file_paths[0]),
        (data.avalon_metadata[1], data.avalon_metadata_file_paths[1]),
        (data.avalon_metadata[2], data.avalon_metadata_file_paths[2]),
    ),
)
def test_format_song_file_paths(metadata, file_path):
    assert util.format_song_file_path(metadata) == file_path
