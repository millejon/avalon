from flask import Flask, render_template, redirect, request
import render_element

app = Flask(__name__)
config_loaded = app.config.from_pyfile('./config.py')


def render_page(content, heading=None):
    playlists = render_element.get_playlists()

    return render_template('page.jinja', playlists=playlists,
                           content=content, heading=heading)


@app.route('/')
def home_page():
    home = render_template("home.jinja")

    return render_page(content=home, heading='Avalon')


@app.route('/artists/')
def view_all_artists():
    artists_table = render_element.artists_table()

    return render_page(artists_table, 'Artists')


@app.route('/artists/<int:artist_id>/')
def view_artist(artist_id):
    artist_data = render_element.artist_page(artist_id)

    return render_page(content=artist_data)


@app.route('/albums/')
def view_all_albums():
    albums_table = render_element.albums_table()

    return render_page(content=albums_table, heading='Albums')


@app.route('/albums/<int:album_id>/')
def view_album(album_id):
    album_data = render_element.album_page(album_id)

    return render_page(content=album_data)




# Listener for local testing on port 3000.
if __name__ == '__main__':
    app.run(port=3000, debug=True)