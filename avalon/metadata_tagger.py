from flask import Blueprint, flash, redirect, render_template, request, url_for

import avalon.utilities as util
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
    pass