from mutagen import File as MutagenFile
from mutagen.flac import Picture, FLAC
from mutagen.mp3 import MP3
import mutagen.id3 as id3

import avalon.utilities as util
from avalon.data import metadata_modifications as metadata_mods


class Song:
    def __init__(self, path):
        self.path = path
        self.mutagen = MutagenFile(self.path)
        self.metadata = {}

    def add_metadata(self, metadata: dict) -> None:
        """Add metadata to music file."""
        self.metadata = metadata

        if isinstance(self.mutagen, FLAC):
            self.add_metadata_to_flac()
            self.add_album_cover_to_flac()
        elif isinstance(self.mutagen, MP3):
            self.add_metadata_to_mp3()
            self.add_album_cover_to_mp3()

        self.mutagen.save()

    def add_metadata_to_flac(self) -> None:
        """Add metadata to FLAC music file."""
        # Initialize FLAC metadata.
        self.mutagen.clear_pictures()
        self.mutagen.delete()

        for key in self.metadata.keys():
            self.mutagen[key] = self.metadata[key]

    def add_album_cover_to_flac(self) -> None:
        """Add album cover metadata to FLAC music file."""
        cover = Picture()

        with open(f"{util.get_directory(self.path)}/cover.jpg", "rb") as image:
            cover.data = image.read()

        cover.type = id3.PictureType.COVER_FRONT
        cover.mime = "image/jpeg"
        self.mutagen.add_picture(cover)

    def add_metadata_to_mp3(self) -> None:
        """Add metadata to MP3 music file."""
        # Initialize MP3 metadata.
        self.mutagen.tags = id3.ID3()

        for key in self.metadata.keys():
            if key == "album":
                # TALB - Album title field
                self.mutagen["TALB"] = id3.TALB(encoding=1, text=self.metadata[key])
            elif key == "title":
                # TIT2 - Song title field
                self.mutagen["TIT2"] = id3.TIT2(encoding=1, text=self.metadata[key])
            else:
                # TXXX - Custom ID3 metadata fields
                self.mutagen[f"TXXX:{key}"] = id3.TXXX(
                    encoding=1, desc=key, text=self.metadata[key]
                )

    def add_album_cover_to_mp3(self) -> None:
        """Add album cover metadata to MP3 music file."""
        with open(f"{util.get_directory(self.path)}/cover.jpg", "rb") as image:
            self.mutagen["APIC"] = id3.APIC(
                encoding=3, mime="image/jpeg", type=3, data=image.read()
            )

    def rename_file(self) -> None:
        """Rename local music file to correspond with its metadata."""
        filename = util.format_song_filename(
            title=self.metadata["title"], number=self.metadata["track_number"]
        )
        self.path = util.rename_music_file(self.path, filename)

    def extract_metadata(self) -> dict:
        """Extract metadata from music file."""
        if isinstance(self.mutagen, FLAC):
            return self.format_metadata_from_flac()
        elif isinstance(self.mutagen, MP3):
            return self.format_metadata_from_mp3()

    def format_metadata_from_flac(self) -> dict:
        """Format metadata from FLAC music file."""
        metadata = {"length": self.mutagen.info.length}

        for key, value in self.mutagen.items():
            if key in metadata_mods["lists"]:
                metadata[key] = value[0].split("; ")
            elif key in metadata_mods["integers"]:
                metadata[key] = int(value[0])
            elif key in metadata_mods["bools"]:
                metadata[key] = True
            else:
                metadata[key] = value[0]

        return metadata

    def format_metadata_from_mp3(self) -> dict:
        """Format metadata from music file."""
        metadata = {
            "album": self.mutagen["TALB"].text[0],
            "title": self.mutagen["TIT2"].text[0],
            "length": self.mutagen.info.length,
        }

        for key, value in self.mutagen.items():
            if key.startswith("TXXX:"):
                key = key.replace("TXXX:", "")

                if key in metadata_mods["lists"]:
                    metadata[key] = value.text[0].split("; ")
                elif key in metadata_mods["integers"]:
                    metadata[key] = int(value.text[0])
                elif key in metadata_mods["bools"]:
                    metadata[key] = True
                else:
                    metadata[key] = value.text[0]

        return metadata
