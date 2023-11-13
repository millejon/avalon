from flask import Blueprint, flash, render_template, request, session

import avalon.utilities as util

bp = Blueprint("metadata-tagger", __name__, url_prefix="/metadata-tagger")


@bp.route("/input-metadata", methods=("GET", "POST"))
def input_metadata():
    if request.method == "POST":
        if util.is_directory(request.form["directory"]):
            session["directory"] = request.form["directory"]
            songs = util.get_song_file_paths(session["directory"])

            if songs:
                return render_template("input-metadata.html", songs=songs)
            else:
                flash(f"No music files in directory! {session['directory']}")

        else:
            flash(f"Directory does not exist! {request.form['directory']}")

    # If GET request received, processing begins here.
    session.pop("directory", None)  # Clear session["directory"]
    return render_template("input-metadata.html")


@bp.route("/process-metadata", methods=("POST",))
def process_metadata():
    pass
