import os
from flask import Blueprint, current_app

from avalon.song_metadata import SongMetadata
from avalon.metadata_mapper import MetadataMapper

bp = Blueprint("update-database", __name__, url_prefix="/")


@bp.route("/update-database", methods=("GET",))
def update_database() -> None:
    """Update database with metadata extracted from music files in local
    music library.
    """
    music_directory = current_app.config["MUSIC_DIRECTORY"]

    for root, directories, files in os.walk(music_directory):
        for file in files:
            # These are the only acceptable music file formats.
            if file.endswith(".flac") or file.endswith(".mp3"):
                song_path = os.path.join(root, file)
                metadata = SongMetadata(song_path).extract_metadata()
                metadata["path"] = song_path.replace(music_directory, "")
                mapper = MetadataMapper(metadata)

                if not mapper.get_song():
                    mapper.add_album()
                    mapper.add_song()
                    mapper.add_song_artists()

                    if "producers" in metadata.keys():
                        mapper.add_producers()

    return "Database update complete!"
