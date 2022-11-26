import mariadb as db
from config import config
from queries import queries


def connect():
    return db.connect(
        host=config['HOST'],
        port=config['PORT'],
        database=config['DATABASE'],
        user=config['USER'],
        password=config['PASSWORD']
        )


def execute_read_query(query, data=None):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query, data)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


def execute_write_query(query, data=None):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()

    cursor.close()
    connection.close()


def get_artist_id(name):
    query = queries['get_artist']
    data = (name,)
    artist_id = execute_read_query(query, data)

    if len(artist_id) == 0:
        return None
    else:
        return artist_id[0][0]


def is_producer(artist):
    producers = ['The Alchemist', 'Harry Fraud']

    if artist in producers:
        return 1
    else:
        return 0


def add_artist(artist):
    artist_id = get_artist_id(artist)

    if artist_id is None:
        producer = is_producer(artist)
        query = queries['insert_artist']
        data = (artist, producer)
        execute_write_query(query, data)

        artist_id = get_artist_id(artist)

    return artist_id


def add_artists(artists):
    artist_ids = []

    for artist in artists:
        artist_id = add_artist(artist)
        artist_ids.append(artist_id)

    return artist_ids


def get_album_id(artist, album):
    query = queries['get_album']
    data = (artist, album)
    album_id = execute_read_query(query, data)

    if len(album_id) == 0:
        return None
    else:
        return album_id[0][0]


def get_last_added_album_id():
    query = queries['get_last_album_id']
    album_id = execute_read_query(query)

    return album_id[0][0]


def add_album(song):
    album_id = get_album_id(song.album_artists[0], song.album)

    if album_id is None:
        query = queries['insert_album']
        data = (song.album, song.single, song.mixtape, song.multi_disc)
        execute_write_query(query, data)

        album_id = get_last_added_album_id()

    return album_id


def does_link_exist(artist, album):
    query = queries['get_artist_album_link']
    data = (artist, album)
    link = execute_read_query(query, data)

    if len(link) == 0:
        return False
    else:
        return True


def add_artist_album_link(artists, album):
    query = queries['insert_artist_album_link']

    for artist in artists:
        if not does_link_exist(artist, album):
            data = (artist, album)
            execute_write_query(query, data)


def get_disc_id(album, disc):
    query = queries['get_disc']
    data = (album, disc)
    disc_id = execute_read_query(query, data)

    if len(disc_id) == 0:
        return None
    else:
        return disc_id[0][0]


def add_disc(album, song):
    disc_id = get_disc_id(album, song.disc_number)

    if disc_id is None:
        query = queries['insert_disc']
        data = (album, song.disc_number, song.disc_title)
        execute_write_query(query, data)

        disc_id = get_disc_id(album, song.disc_number)

    return disc_id


def get_song_id(path):
    query = queries['get_song']
    data = (path,)
    song_id = execute_read_query(query, data)

    if len(song_id) == 0:
        return None
    else:
        return song_id[0][0]


def add_song(song, album, disc):
    query = queries['insert_song']
    data = (album, disc, song.track_number, song.title, song.length,
            song.release_date, song.path, song.bonus_track)
    execute_write_query(query, data)

    song_id = get_song_id(song.path)

    return song_id


def add_artist_song_link(artists, song, group_member):
    query = queries['insert_artist_song_link']

    for artist in artists:
        data = (artist, song, group_member)
        execute_write_query(query, data)
