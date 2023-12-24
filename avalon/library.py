from flask import Blueprint, render_template

import avalon.database as db
from avalon.artist import Artist
from avalon.album import Album
from avalon.data import database

bp = Blueprint("library", __name__, url_prefix="/")


@bp.route("/artists/", methods=("GET",))
def view_all_artists():
    artists_data = db.execute_read_query(
        query=database["artists"]["queries"]["read"]["all_artists"]
    )
    artists = [Artist(data["id"]) for data in artists_data]

    return render_template("all_artists.html", artists=artists)


@bp.route("/artists/<int:id>", methods=("GET",))
def view_artist(id):
    return render_template("artist.html", artist=Artist(id))


@bp.route("/albums/", methods=("GET",))
def view_all_albums():
    albums_data = db.execute_read_query(
        query=database["albums"]["queries"]["read"]["all_albums"]
    )
    albums = [Album(data["id"]) for data in albums_data]

    return render_template("all_albums.html", albums=albums)


@bp.route("/albums/<int:id>", methods=("GET",))
def view_album(id):
    return render_template("album.html", album=Album(id))
