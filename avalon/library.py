from flask import Blueprint, redirect, render_template, request, send_file, url_for

import avalon.database as db
from avalon.artist import Artist
from avalon.album import Album
from avalon.playlist import Playlist
from avalon.hub import Hub
from avalon.data import database

bp = Blueprint("library", __name__, url_prefix="/")


def render_page(template: str, content, key: str = None):
    return render_template(
        template, content=content, key=key, playlists=get_playlists()
    )


@bp.route("/", methods=("GET",))
def home():
    return redirect(url_for("library.view_all_artists"))


@bp.route("/artists/", methods=("GET",))
def view_all_artists():
    artists_data = db.execute_read_query(
        query=database["artists"]["queries"]["read"]["all_artists"]
    )
    artists = [Artist(data["id"]) for data in artists_data]

    return render_page(template="all_artists.html", content=artists, key="artists")


@bp.route("/artists/<int:id>", methods=("GET",))
def view_artist(id: int):
    return render_page(template="artist.html", content=Artist(id), key="artists")


@bp.route("/artists/<int:id>/songs/", methods=("GET",))
def view_artist_songs(id: int):
    return render_page(template="artist_songs.html", content=Artist(id), key="artists")


@bp.route("/artists/<int:id>/songs/download/", methods=("GET",))
def download_artist_songs(id: int):
    Playlist.download_playlist(Artist(id).songs)
    return send_file("static/playlist.m3u", as_attachment=True)


@bp.route("/artists/<int:id>/produced/", methods=("GET",))
def view_artist_produced_songs(id: int):
    return render_page(template="artist_produced_songs.html", content=Artist(id))


@bp.route("/artists/<int:id>/produced/download/", methods=("GET",))
def download_artist_produced_songs(id: int):
    Playlist.download_playlist(Artist(id).produced_songs)
    return send_file("static/playlist.m3u", as_attachment=True)


@bp.route("/artists/<int:id>/<album_type>/", methods=("GET",))
def view_artist_albums(id: int, album_type: str):
    return render_page(
        template="artist_albums.html", content=Artist(id), key=album_type
    )


@bp.route("/albums/", methods=("GET",))
def view_all_albums():
    albums_data = db.execute_read_query(
        query=database["albums"]["queries"]["read"]["all_albums"]
    )
    albums = [Album(data["id"]) for data in albums_data]

    return render_page(template="all_albums.html", content=albums)


@bp.route("/albums/<int:id>", methods=("GET",))
def view_album(id: int):
    return render_page(template="album.html", content=Album(id))


@bp.route("/albums/<int:id>/download/", methods=("GET",))
def download_album_songs(id: int):
    Playlist.download_playlist(Album(id).songs)
    return send_file("static/playlist.m3u", as_attachment=True)


@bp.route("/playlists/<int:id>", methods=("GET",))
def view_playlist(id: int):
    return render_page("playlist.html", content=Playlist(id))


@bp.route("/playlists/<int:id>/download/", methods=("GET",))
def download_playlist(id: int):
    Playlist.download_playlist(Playlist(id).songs)
    return send_file("static/playlist.m3u", as_attachment=True)


@bp.route("/playlists/create/", methods=("POST",))
def create_playlist():
    db.execute_write_query(
        query=database["playlists"]["queries"]["write"]["add"],
        data=(request.form["playlist_title"],),
    )

    return redirect(request.referrer)


@bp.route("/playlists/<int:playlist_id>/songs/<int:song_id>", methods=("GET",))
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


@bp.route("/hubs/", methods=("GET",))
def view_all_hubs():
    hubs_data = db.execute_read_query(
        query=database["hubs"]["queries"]["read"]["all_hubs"]
    )
    hubs = [Hub(data["id"]) for data in hubs_data]

    return render_page(template="all_artists.html", content=hubs, key="hubs")


@bp.route("/hubs/<int:id>", methods=("GET",))
def view_hub(id: int):
    return render_page(template="artist.html", content=Hub(id), key="hubs")


@bp.route("/hubs/<int:id>/songs/", methods=("GET",))
def view_hub_songs(id: int):
    return render_page(template="artist_songs.html", content=Hub(id), key="hubs")


@bp.route("/hubs/<int:id>/songs/download/", methods=("GET",))
def download_hub_songs(id: int):
    Playlist.download_playlist(Hub(id).songs)
    return send_file("static/playlist.m3u", as_attachment=True)


@bp.route("/hubs/<int:id>/albums/", methods=("GET",))
def view_hub_albums(id: int):
    return render_page(template="artist_albums.html", content=Hub(id), key="albums")
