from flask import Blueprint, flash, redirect, render_template, request, url_for

import avalon.utilities as util
from avalon.song import Song
from avalon.data import required_metadata_input_fields as required_fields

bp = Blueprint("metadata-tagger", __name__, url_prefix="/metadata-tagger")


@bp.route("/input-metadata", methods=("GET", "POST"))
def input_metadata():
    if request.method == "POST":
        if util.is_directory(request.form["directory"]):
            songs = util.get_song_file_paths(request.form["directory"])

            if songs:
                return render_template("input-metadata.html", songs=songs)
            else:
                flash(f"No music files in directory! {request.form['directory']}")

        else:
            flash(f"Directory does not exist! {request.form['directory']}")

    # If GET request received, processing begins here.
    return render_template("input-metadata.html")


@bp.route("/process-metadata", methods=("POST",))
def process_metadata():
    try:
        validate_metadata_form(request.form)
    except ExceptionGroup as error:
        flash(error.message)
        for exception in error.exceptions:
            flash(str(exception))
    else:
        process_songs(metadata=format_metadata(request.form))
    finally:
        return redirect(url_for("metadata-tagger.input_metadata"))


def validate_metadata_form(form: dict) -> None:
    """Validate user's submitted metadata form."""
    exceptions = []

    validate_album_metadata(form, exceptions)
    validate_song_metadata(form, exceptions)

    if "multidisc" in form.keys():
        validate_multidisc_metadata(form, exceptions)
    elif form["disc_name"] or form["disc_number"]:
        exceptions.append(ValueError("Value for 'multidisc' is missing!"))
        validate_multidisc_metadata(form, exceptions)

    if exceptions:
        raise ExceptionGroup("Invalid metadata form submitted! Please check "
                             "data and resubmit form!", exceptions)


def validate_album_metadata(form: dict, exceptions: list[ValueError]) -> None:
    """Validate user's submitted album metadata."""
    for field in required_fields["album"]:
        if not form[field]:
            exceptions.append(ValueError(f"Value for '{field}' is missing!"))


def validate_song_metadata(form: dict, exceptions: list[ValueError]) -> None:
    """Validate user's submitted song metadata."""
    for x in range(int(form["track_count"])):
        prefix = f"track{x+1}_"
        for field in required_fields["song"]:
            if not form[f"{prefix}{field}"]:
                exceptions.append(ValueError(f"Value for '{prefix}{field}' "
                                             "is missing!"))

        if ((form[f"{prefix}coproducers"] or form[f"{prefix}additional_producers"])
                and not form[f"{prefix}producers"]):
            exceptions.append(ValueError(f"Value for '{prefix}producers' is missing!"))


def validate_multidisc_metadata(form: dict, exceptions: list[ValueError]) -> None:
    """Validate user's submitted multidisc metadata."""
    if "single" in form.keys():
        exceptions.append(ValueError("An album can not be a single and multidisc!"))
    if not form["disc_name"]:
        exceptions.append(ValueError("Value for 'disc_name' is missing!"))
    if not form["disc_number"]:
        exceptions.append(ValueError("Value for 'disc_number' is missing!"))


def format_metadata(form: dict) -> list[dict]:
    """Return formatted data from user's submitted metadata form in a
    list of dictionaries where each dictionary contains the metadata
    for one song.
    """
    metadata = []

    for x in range(int(form["track_count"])):
        metadata.append({"track_number": f"{x+1}"})
        prefix = f"track{x+1}_"

        for key, value in form.items():
            if key.startswith(prefix):
                metadata[x][key.replace(prefix, "")] = value
            elif key.startswith("track"):
                # Ignore song-specific metadata for other songs.
                continue
            else:
                metadata[x][key] = value

    return metadata


def process_songs(metadata: dict) -> None:
    """Add metadata to music files and rename the music files to
    correspond with the metadata.
    """
    for track in metadata:
        song = Song(metadata[track]["path"])
        metadata[track].pop("path")

        song.add_metadata(metadata[track])
        song.rename_file()
