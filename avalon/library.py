from flask import Blueprint, render_template

import avalon.database as db
from avalon.artist import Artist
from avalon.data import database

bp = Blueprint("library", __name__, url_prefix="/")


@bp.route("/artists", methods=("GET",))
def view_all_artists():
    artists_data = db.execute_read_query(
        query=database["artists"]["queries"]["read"]["all_artists"]
    )
    artists = [Artist(data["id"]) for data in artists_data]

    return render_template("all_artists.html", artists=artists)


@bp.route("/artists/<int:id>", methods=("GET",))
def view_artist(id):
    return render_template("artist.html", artist=Artist(id))
