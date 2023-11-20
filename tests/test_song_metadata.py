import pytest
import os
from mutagen.flac import FLAC
from mutagen.mp3 import MP3

from avalon.song_metadata import SongMetadata
from tests.data import song_metadata, avalon_metadata, dummy_files


# Initializing an instance of the SongMetadata class should set the path
# property of the instance to the path passed at initialization, set
# the mutagen property to an instance of either the Mutagen FLAC class
# or the mutagen MP3 class, and set the metadata property to an empty
# dictionary.
@pytest.mark.parametrize("suffix, object_type", ((".flac", FLAC), (".mp3", MP3)))
def test_initialize_song_instance(dummy_file, suffix, object_type):
    file_path = dummy_file(suffix)
    song = SongMetadata(file_path)

    assert song.path == file_path
    assert isinstance(song.mutagen, object_type)
    assert song.data == {}


# add_metadata_to_flac() should properly tag FLAC file with the
# metadata passed. Tagging the album cover is handled by a separate
# function so the FLAC file should not have an album cover tag.
@pytest.mark.parametrize("metadata", song_metadata)
def test_add_metadata_to_flac(dummy_file, metadata):
    song = SongMetadata(dummy_file(".flac"))
    song.data = metadata

    song.add_metadata_to_flac()

    assert len(song.mutagen.keys()) == len(metadata.keys())
    assert not song.mutagen.pictures
    for key in metadata.keys():
        assert song.mutagen[key][0] == metadata[key]


# add_album_cover_to_flac() should properly tag FLAC file with the album
# cover. Tagging the rest of the metadata is handled by a separate
# function so the FLAC file should not have any other metadata.
def test_add_album_cover_to_flac(dummy_file):
    song = SongMetadata(dummy_file(".flac"))
    dummy_file(".jpg")

    song.add_album_cover_to_flac()

    assert song.mutagen.pictures
    assert len(song.mutagen.pictures) == 1
    assert song.mutagen.pictures[0].data == dummy_files[".jpg"]
    assert len(song.mutagen.keys()) == 0


# add_metadata_to_mp3() should properly tag MP3 file with the metadata
# passed. Tagging the album cover is handled by a separate function so
# the MP3 file should not have an album cover tag.
@pytest.mark.parametrize("metadata", song_metadata)
def test_add_metadata_to_mp3(dummy_file, metadata):
    song = SongMetadata(dummy_file(".mp3"))
    song.data = metadata

    song.add_metadata_to_mp3()

    assert len(song.mutagen.keys()) == len(metadata.keys())
    assert "APIC" not in song.mutagen.keys()
    for key in metadata.keys():
        if key == "album":
            assert song.mutagen["TALB"].text[0] == metadata["album"]
        elif key == "title":
            assert song.mutagen["TIT2"].text[0] == metadata["title"]
        else:
            assert song.mutagen[f"TXXX:{key}"].text[0] == metadata[key]


# add_album_cover_to_mp3() should properly tag MP3 file with the album
# cover. Tagging the rest of the metadata is handled by a separate
# function so the MP3 file should not have any other metadata.
def test_add_album_cover_to_mp3(dummy_file):
    song = SongMetadata(dummy_file(".mp3"))
    dummy_file(".jpg")

    song.add_album_cover_to_mp3()

    assert list(song.mutagen.keys()) == ["APIC"]
    assert song.mutagen["APIC"].data == dummy_files[".jpg"]


# add_metadata() should properly tag music file with the metadata passed
# and the album cover.
@pytest.mark.parametrize("metadata", song_metadata)
def test_add_metadata_flac(dummy_file, metadata):
    song = SongMetadata(dummy_file(".flac"))
    dummy_file(".jpg")

    song.add_metadata(metadata)

    assert len(song.mutagen.keys()) == len(metadata.keys())
    assert song.mutagen.pictures
    assert len(song.mutagen.pictures) == 1
    assert song.mutagen.pictures[0].data == dummy_files[".jpg"]
    for key in metadata.keys():
        assert song.mutagen[key][0] == metadata[key]


@pytest.mark.parametrize("metadata", song_metadata)
def test_add_metadata_mp3(dummy_file, metadata):
    song = SongMetadata(dummy_file(".mp3"))
    dummy_file(".jpg")

    song.add_metadata(metadata)

    assert len(song.mutagen.keys()) == len(metadata.keys()) + 1
    assert "APIC" in song.mutagen.keys()
    assert song.mutagen["APIC"].data == dummy_files[".jpg"]
    for key in metadata.keys():
        if key == "album":
            assert song.mutagen["TALB"].text[0] == metadata["album"]
        elif key == "title":
            assert song.mutagen["TIT2"].text[0] == metadata["title"]
        else:
            assert song.mutagen[f"TXXX:{key}"].text[0] == metadata[key]


# rename_file() should rename the local music file to correspond with
# the song's metadata.
@pytest.mark.parametrize(
    ("metadata, suffix, renamed"),
    (
        (song_metadata[0], ".flac", "02_in_my_lifetime.flac"),
        (song_metadata[1], ".mp3", "08_affirmative_action.mp3"),
        (song_metadata[2], ".flac", "03_impossible.flac"),
    ),
)
def test_rename_file(dummy_file, metadata, suffix, renamed):
    song = SongMetadata(dummy_file(suffix))
    directory = os.path.dirname(song.path)
    song.data = metadata
    prior_path = song.path

    song.rename_file()

    assert not os.path.isfile(prior_path), f"{prior_path} still exists in {directory}"
    assert os.path.isfile(
        f"{song.path}"
    ), f"{prior_path} was not renamed to {renamed} in {directory}"


# format_metadata_from_flac() should format and return the metadata
# from a FLAC file. Formatting involves splitting fields that can have
# multiple values into lists, converting numerical values to integers,
# and converting "True" values into bools.
@pytest.mark.parametrize(
    ["raw", "formatted"],
    (
        (song_metadata[0], avalon_metadata[0]),
        (song_metadata[1], avalon_metadata[1]),
        (song_metadata[2], avalon_metadata[2]),
    ),
)
def test_format_metadata_from_flac(dummy_file, raw, formatted):
    song = SongMetadata(dummy_file(".flac"))
    song.data = raw
    song.add_metadata_to_flac()

    assert song.format_metadata_from_flac() == formatted


# format_metadata_from_mp3() should format and return the metadata
# from a MP3 file. Formatting involves splitting fields that can have
# multiple values into lists, converting numerical values to integers,
# and converting "True" values into bools.
@pytest.mark.parametrize(
    ["raw", "formatted"],
    (
        (song_metadata[0], avalon_metadata[0]),
        (song_metadata[1], avalon_metadata[1]),
        (song_metadata[2], avalon_metadata[2]),
    ),
)
def test_format_metadata_from_mp3(dummy_file, raw, formatted):
    song = SongMetadata(dummy_file(".mp3"))
    song.data = raw
    song.add_metadata_to_mp3()

    assert song.format_metadata_from_mp3() == formatted
