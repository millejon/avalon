from flask import Flask, render_template, redirect, request
from queries import queries
import db_operations as db
import render_element

app = Flask(__name__)
config_loaded = app.config.from_pyfile('./config.py')


def render_page(content, heading=None):
    query = queries['get_playlists']
    playlists = db.query_database(query)

    return render_template('page.jinja', playlists=playlists,
                           content=content, heading=heading)


@app.route('/')
def home_page():
    home = render_template("home.jinja")

    return render_page(content=home, heading='Avalon')


@app.route('/artists/')
def view_all_artists():
    query = queries['get_all_artists']
    artists = db.query_database(query)
    artists_table = render_element.artists_table(artists)

    return render_page(artists_table, 'Artists')


@app.route('/artists/<int:artist_id>/')
def view_artist(artist_id):
    artist_data = render_element.artist_page(artist_id)

    return render_page(content=artist_data)


@app.route('/albums/')
def view_all_albums():
    query = queries['get_all_albums']
    albums = db.query_database(query)
    albums_table = render_element.albums_table(albums)

    return render_page(content=albums_table, heading='Albums')


@app.route('/albums/<int:album_id>/')
def view_album(album_id):
    album_data = render_element.album_page(album_id)

    return render_page(content=album_data)


@app.route('/playlists/<int:playlist_id>/')
def view_playlist(playlist_id):
    name = render_element.get_playlist_name(playlist_id)
    songs = render_element.playlist_songs_table(playlist_id)

    return render_page(content=songs, heading=name)


@app.route('/playlists/create/', methods=['GET'])
def create_playlist():
    name = request.args.get('playlist_name')
    db.create_playlist(name)

    return redirect(request.referrer)


@app.route('/playlists/add/', methods=['GET'])
def add_song_to_playlist():
    add_song = request.args.get('add_song').split("_")
    db.add_song_to_playlist(add_song[0], add_song[1])

    return redirect(request.referrer)


@app.route('/playlists/<int:playlist>/delete/<int:song>/', methods=['GET'])
def delete_song_from_playlist(playlist, song):
    db.delete_song_from_playlist(playlist, song)

    return redirect(request.referrer)


@app.route('/search/', methods=['GET'])
def search_database():
    search_term = request.args.get('search')
    search_results = render_element.search_results(search_term)

    return render_page(content=search_results, heading="Search Results")


# Listener for local testing on port 3000.
if __name__ == '__main__':
    app.run(port=3000, debug=True)
