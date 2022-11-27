from flask import render_template
from queries import queries
import mariadb
import os
import requests
import db_operations as db

months = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December',
}

string_formatting = {
    ' / ': '_',
    ' ': '_',
    '.': '',
    ',': '',
    '/': '',
    "'": '',
}


def format_string(string):
    for key, value in string_formatting.items():
        string = string.replace(key, value)

    return string.lower()


def get_artist_image(artist):
    artist_name = format_string(artist)

    if os.path.exists(f'./static/img/artists/{artist_name}.jpg'):
        return f'artists/{artist_name}.jpg'
    else:
        return f'artists/default.jpg'


def get_album_cover(artist, album):
    artist_name = format_string(artist)
    album_name = format_string(album)

    return f'albums/{artist_name}/{album_name}.jpg'


def convert_seconds_to_minutes(length):
    minutes = int(length) // 60
    seconds = int(length) - (minutes * 60)

    if seconds < 10:
        seconds = '{:02d}'.format(seconds)

    return f'{minutes}:{seconds}'


def get_artists():
    query = queries['get_all_artists']
    results = db.execute_read_query(query)

    return results


def artists_table():
    artists = get_artists()
    number_of_artists = len(artists)

    for x in range(number_of_artists):
        artists[x] = list(artists[x])
        artist_image = get_artist_image(artists[x][1])
        artists[x].insert(0, artist_image)

    return render_template('all_artists.jinja', artists=artists)


def get_all_albums():
    query = queries['get_all_albums']
    results = db.execute_read_query(query)

    return results


def get_album_artists(album):
    query = queries['get_album_artists']
    data = (album,)
    results = db.execute_read_query(query, data)

    return results


def albums_table(albums=None):
    if albums is None:
        albums = get_all_albums()

    number_of_albums = len(albums)

    for x in range(number_of_albums):
        albums[x] = list(albums[x])
        album_cover = get_album_cover(albums[x][2], albums[x][1])
        albums[x].insert(0, album_cover)

        albums[x][3] = get_album_artists(albums[x][1])

    return render_template('albums.jinja', albums=albums)


def get_artist_albums(artist, single, mixtape):
    query = queries['get_artist_albums']
    data = (artist, single, mixtape)
    results = db.execute_read_query(query, data)

    if len(results) == 0:
        return None
    else:
        return albums_table(results)


def get_artist_songs(artist):
    query = queries['get_artist_songs']
    data = (artist,)
    results = db.execute_read_query(query, data)

    return results


def get_song_artists(song):
    query = queries['get_song_artists']
    data = (song,)
    results = db.execute_read_query(query, data)

    return results


def prepare_song_data(songs):
    number_of_songs = len(songs)

    for x in range(number_of_songs):
        songs[x] = list(songs[x])
        song_artists = get_song_artists(songs[x][0])
        songs[x].insert(3, song_artists)

        if int(songs[x][4]) > 1:
            songs[x][4] = convert_seconds_to_minutes(songs[x][4])
        else:
            songs[x][4] = ''

    return songs


def get_playlists():
    query = queries['get_playlists']
    results = db.execute_read_query(query)

    if len(results) == 0:
        return None
    else:
        return results


def artist_songs_table(songs):
    songs = prepare_song_data(songs)
    playlists = get_playlists()

    return render_template('songs.jinja', songs=songs, playlists=playlists)


def get_artist_info(artist):
    query = queries['get_artist_info']
    data = (artist,)
    results = db.execute_read_query(query, data)

    return results


def get_artist_bio(artist):
    """This function calls the microservice implemented by my team member."""
    response = requests.get("https://cs361.onrender.com/artist", params={
        "name": artist})
    response_json = response.json()

    return response_json["text"]


def get_artist_discography(artist):
    songs = get_artist_songs(artist)
    songs_table = artist_songs_table(songs)
    albums = get_artist_albums(artist, 0, 0)
    singles = get_artist_albums(artist, 1, 0)
    mixtapes = get_artist_albums(artist, 0, 1)

    return [songs_table, albums, singles, mixtapes]


def artist_page(artist):
    artist_name = get_artist_info(artist)[0][1]
    artist_image = get_artist_image(artist_name)
    artist_bio = get_artist_bio(artist_name)
    artist_info = [artist_name, artist_image, artist_bio]

    discography = get_artist_discography(artist)

    return render_template('view_artist.jinja', artist_info=artist_info,
                           discography=discography)


def get_album_info(album):
    query = queries['get_album_info']
    data = (album,)
    results = db.execute_read_query(query, data)

    return list(results[0])


def album_header(album):
    album_info = get_album_info(album)
    album_artists = get_album_artists(album)
    album_info.insert(1, album_artists)

    cover = get_album_cover(album_info[1][0][1], album_info[0])
    album_info.insert(0, cover)

    album_info[5] = convert_seconds_to_minutes(album_info[5])
    album_info[6] = album_info[6].strftime("%B %#d, %Y")

    return album_info


def get_album_songs(album):
    query = queries['get_album_songs']
    data = (album,)
    results = db.execute_read_query(query, data)

    return results


def album_songs_table(songs):
    songs = prepare_song_data(songs)
    playlists = get_playlists()

    return render_template('album_songs.jinja', songs=songs,
                           playlists=playlists)


def single_album_tracklist(album):
    songs = get_album_songs(album)
    songs_table = album_songs_table(songs)

    return [songs_table]


def get_disc_info(album):
    query = queries['get_disc_info']
    data = (album,)
    results = db.execute_read_query(query, data)

    return results


def get_disc_songs(disc):
    query = queries['get_songs_on_disc']
    data = (disc,)
    results = db.execute_read_query(query, data)

    return results


def single_disc_table(disc):
    songs = get_disc_songs(disc)

    return album_songs_table(songs)


def multi_disc_album_tracklist(album):
    disc_info = get_disc_info(album)
    disc_tracklist = []

    for disc in disc_info:
        disc_table = single_disc_table(disc[0])
        disc = [disc[1], disc_table]
        disc_tracklist.append(disc)

    return disc_tracklist


def get_bonus_songs(album):
    query = queries['get_album_bonus_songs']
    data = (album,)
    results = db.execute_read_query(query, data)

    return results


def bonus_songs_tracklist(album):
    bonus_songs = get_bonus_songs(album)

    if len(bonus_songs) == 0:
        return None
    else:
        bonus_songs_table = album_songs_table(bonus_songs)

        return bonus_songs_table


def album_page(album):
    album_info = album_header(album)

    if album_info[3] == 0:
        songs = single_album_tracklist(album)
    else:
        songs = multi_disc_album_tracklist(album)

    bonus_songs = bonus_songs_tracklist(album)

    return render_template('view_album.jinja', album_info=album_info,
                           songs=songs, bonus_songs=bonus_songs)








