import pytest
import os
from mutagen import File as MutagenFile

from avalon.song import Song
from tests.data import song_metadata, dummy_files


# Initializing an instance of the Song class should set the path
# property of the instance to the path passed at initialization and set
# the metadata property to an empty dictionary.
@pytest.mark.parametrize("suffix", [".flac", ".mp3"])
def test_initialize_song_instance(suffix, dummy_file):
    file_path = dummy_file(suffix)
    song = Song(file_path)
    assert song.path == file_path
    assert song.metadata == {}


# add_metadata_to_flac() should properly tag FLAC file with the
# metadata passed. Tagging the album cover is handled by a separate
# function so the FLAC file should not have an album cover tag.
@pytest.mark.parametrize("metadata", song_metadata)
def test_add_metadata_to_flac(metadata, dummy_file):
    flac_file_path = dummy_file(".flac")
    song = Song(flac_file_path)
    song.metadata = metadata
    flac = MutagenFile(flac_file_path)

    song.add_metadata_to_flac(flac)

    assert len(flac.keys()) == len(metadata.keys())
    assert not flac.pictures
    for key in metadata.keys():
        assert flac[key][0] == metadata[key]


# add_album_cover_to_flac() should properly tag FLAC file with the album
# cover. Tagging the rest of the metadata is handled by a separate
# function so the FLAC file should not have any other metadata.
def test_add_album_cover_to_flac(dummy_file):
    flac_file_path = dummy_file(".flac")
    dummy_file('.jpg')
    song = Song(flac_file_path)
    flac = MutagenFile(flac_file_path)

    song.add_album_cover_to_flac(flac)

    assert flac.pictures
    assert len(flac.pictures) == 1
    assert flac.pictures[0].data == dummy_files[".jpg"]
    assert len(flac.keys()) == 0


# add_metadata_to_mp3() should properly tag MP3 file with the metadata
# passed. Tagging the album cover is handled by a separate function so
# the MP3 file should not have an album cover tag.
@pytest.mark.parametrize("metadata", song_metadata)
def test_add_metadata_to_mp3(metadata, dummy_file):
    mp3_file_path = dummy_file(".mp3")
    song = Song(mp3_file_path)
    song.metadata = metadata
    mp3 = MutagenFile(mp3_file_path)

    song.add_metadata_to_mp3(mp3)

    assert len(mp3.keys()) == len(metadata.keys())
    assert "APIC" not in mp3.keys()
    for key in metadata.keys():
        if key == "album":
            assert mp3["TALB"].text[0] == metadata["album"]
        elif key == "title":
            assert mp3["TIT2"].text[0] == metadata["title"]
        else:
            assert mp3[f"TXXX:{key}"].text[0] == metadata[key]


# add_album_cover_to_mp3() should properly tag MP3 file with the album
# cover. Tagging the rest of the metadata is handled by a separate
# function so the MP3 file should not have any other metadata.
def test_add_album_cover_to_mp3(dummy_file):
    mp3_file_path = dummy_file(".mp3")
    dummy_file('.jpg')
    song = Song(mp3_file_path)
    mp3 = MutagenFile(mp3_file_path)

    song.add_album_cover_to_mp3(mp3)

    assert list(mp3.keys()) == ["APIC"]
    assert mp3["APIC"].data == dummy_files[".jpg"]


# add_metadata() should properly tag music file with the metadata passed
# and the album cover.
@pytest.mark.parametrize("metadata", song_metadata)
def test_add_metadata_flac(metadata, dummy_file):
    flac_file_path = dummy_file(".flac")
    dummy_file(".jpg")
    song = Song(flac_file_path)

    song.add_metadata(metadata)

    flac = MutagenFile(song.path)
    assert len(flac.keys()) == len(metadata.keys())
    assert flac.pictures
    assert len(flac.pictures) == 1
    assert flac.pictures[0].data == dummy_files[".jpg"]
    for key in metadata.keys():
        assert flac[key][0] == metadata[key]


@pytest.mark.parametrize("metadata", song_metadata)
def test_add_metadata_mp3(metadata, dummy_file):
    mp3_file_path = dummy_file(".mp3")
    dummy_file(".jpg")
    song = Song(mp3_file_path)

    song.add_metadata(metadata)

    mp3 = MutagenFile(song.path)
    assert len(mp3.keys()) == len(metadata.keys()) + 1
    assert "APIC:" in mp3.keys()
    assert mp3["APIC:"].data == dummy_files[".jpg"]
    for key in metadata.keys():
        if key == "album":
            assert mp3["TALB"].text[0] == metadata["album"]
        elif key == "title":
            assert mp3["TIT2"].text[0] == metadata["title"]
        else:
            assert mp3[f"TXXX:{key}"].text[0] == metadata[key]


# rename_file() should rename the local music file to correspond with
# the song's metadata.
@pytest.mark.parametrize(("metadata, suffix, renamed"), (
    (song_metadata[0], ".flac", "02_in_my_lifetime.flac"),
    (song_metadata[1], ".mp3", "08_affirmative_action.mp3"),
    (song_metadata[2], ".flac", "03_impossible.flac"),
))
def test_rename_file(metadata, suffix, renamed, dummy_file):
    file_path = dummy_file(suffix)
    directory = os.path.dirname(file_path)
    song = Song(file_path)
    song.metadata = metadata

    song.rename_file()

    assert not os.path.isfile(file_path), f"{file_path} still exists in {directory}"
    assert os.path.isfile(f"{directory}/{renamed}"), \
        f"{file_path} was not renamed to {renamed} in {directory}"
