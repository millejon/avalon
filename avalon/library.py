from flask import Blueprint, redirect, render_template, request

import avalon.database as db
from avalon.artist import Artist
from avalon.album import Album
from avalon.playlist import Playlist
from avalon.data import database

bp = Blueprint("library", __name__, url_prefix="/")


def render_page(template: str, content):
    return render_template(template, content=content, playlists=get_playlists())


@bp.route("/artists/", methods=("GET",))
def view_all_artists():
    artists_data = db.execute_read_query(
        query=database["artists"]["queries"]["read"]["all_artists"]
    )
    artists = [Artist(data["id"]) for data in artists_data]

    return render_page(template="all_artists.html", content=artists)


@bp.route("/artists/<int:id>/", methods=("GET",))
def view_artist(id: int):
    return render_page(template="artist.html", content=Artist(id))


@bp.route("/albums/", methods=("GET",))
def view_all_albums():
    albums_data = db.execute_read_query(
        query=database["albums"]["queries"]["read"]["all_albums"]
    )
    albums = [Album(data["id"]) for data in albums_data]

    return render_page(template="all_albums.html", content=albums)


@bp.route("/albums/<int:id>/", methods=("GET",))
def view_album(id: int):
    return render_page(template="album.html", content=Album(id))


@bp.route("/playlists/<int:id>/", methods=("GET",))
def view_playlist(id: int):
    return render_page("playlist.html", content=Playlist(id))


@bp.route("/playlists/create/", methods=("POST",))
def create_playlist():
    db.execute_write_query(
        query=database["playlists"]["queries"]["write"],
        data=(request.form["playlist_name"],),
    )

    return redirect(request.referrer)


@bp.route("/playlists/<int:playlist_id>/songs/<int:song_id>/", methods=("POST",))
def add_song_to_playlist(playlist_id: int, song_id: int):
    Playlist(playlist_id).add_song(song_id)

    return redirect(request.referrer)


@bp.route("/playlists/<int:playlist_id>/songs/<int:song_id>/delete/", methods=("POST",))
def delete_song_from_playlist(playlist_id: int, song_id: int):
    Playlist(playlist_id).delete_song(song_id)

    return redirect(request.referrer)


def get_playlists() -> list[Playlist]:
    playlists_data = db.execute_read_query(
        query=database["playlists"]["queries"]["read"]["all_playlists"]
    )

    return [Playlist(data["id"]) for data in playlists_data]
