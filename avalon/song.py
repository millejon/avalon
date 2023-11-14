from mutagen import File as MutagenFile
from mutagen.flac import Picture, FLAC
from mutagen.mp3 import MP3
import mutagen.id3 as id3

import avalon.utilities as util


class Song:
    def __init__(self, path):
        self.path = path

    def add_metadata(self, metadata: dict) -> None:
        """Add metadata to music file."""
        song = MutagenFile(self.path)

        if isinstance(song, FLAC):
            self.add_metadata_to_flac(song, metadata)
            self.add_album_cover_to_flac(song)
        elif isinstance(song, MP3):
            self.add_metadata_to_mp3(song, metadata)
            self.add_album_cover_to_mp3(song)

        song.save()

    def add_metadata_to_flac(self, song: FLAC, metadata: dict) -> None:
        """Add metadata to FLAC music file."""
        # Initialize FLAC metadata.
        song.clear_pictures()
        song.delete()

        for key in metadata.keys():
            song[key] = metadata[key]

    def add_album_cover_to_flac(self, song: FLAC) -> None:
        """Add album cover metadata to FLAC music file."""
        cover = Picture()

        with open(f"{util.get_directory(self.path)}\\cover.jpg", "rb") as image:
            cover.data = image.read()

        cover.type = id3.PictureType.COVER_FRONT
        cover.mime = "image/jpeg"
        song.add_picture(cover)

    def add_metadata_to_mp3(self, song: MP3, metadata: dict) -> None:
        """Add metadata to MP3 music file."""
        # Initialize MP3 metadata.
        song.tags = id3.ID3()

        for key in metadata.keys():
            if key == "album":
                # TALB - Album title field
                song["TALB"] = id3.TALB(encoding=1, text=metadata[key])
            elif key == "title":
                # TIT2 - Song title field
                song["TIT2"] = id3.TIT2(encoding=1, text=metadata[key])
            else:
                # TXXX - Custom ID3 metadata fields
                song[f"TXXX:{key}"] = id3.TXXX(encoding=1, desc=key,
                                               text=metadata[key])

    def add_album_cover_to_mp3(self, song: MP3) -> None:
        """Add album cover metadata to MP3 music file."""
        with open(f"{util.get_directory(self.path)}/cover.jpg", "rb") as image:
            song["APIC"] = id3.APIC(encoding=3, mime="image/jpeg",
                                    type=3, data=image.read())

    def rename_file(self):
        pass
