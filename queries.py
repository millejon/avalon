queries = {
    'get_artist': '''
        SELECT id, name FROM artists WHERE name = %s;
        ''',
    'insert_artist': '''
        INSERT INTO artists (name, producer)
        VALUES (%s, %s);
        ''',
    'get_album': '''
        SELECT albums.id, albums.name FROM albums
        INNER JOIN artists_albums ON albums.id = artists_albums.album_id
        INNER JOIN artists ON artists_albums.artist_id = artists.id
        WHERE artists.name = %s AND albums.name = %s;
        ''',
    'get_last_album_id': '''
        SELECT id FROM albums
        ORDER BY id DESC LIMIT 1;
        ''',
    'insert_album': '''
        INSERT INTO albums (name, single, mixtape, multi_disc)
        VALUES (%s, %s, %s, %s);
        ''',
    'get_artist_album_link': '''
        SELECT id FROM artists_albums
        WHERE artist_id = %s AND album_id = %s;
        ''',
    'insert_artist_album_link': '''
        INSERT INTO artists_albums (artist_id, album_id)
        VALUES (%s, %s);
        ''',
    'get_disc': '''
        SELECT id, disc_number, name FROM discs
        WHERE album_id = %s AND disc_number = %s;
        ''',
    'insert_disc': '''
        INSERT INTO discs (album_id, disc_number, name)
        VALUES (%s, %s, %s);
        ''',
    'get_song': '''
        SELECT id FROM songs WHERE path = %s;
        ''',
    'insert_song': '''
        INSERT INTO songs (album_id, disc_id, track_number, name, length, 
        date, path, bonus)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        ''',
    'insert_artist_song_link': '''
        INSERT INTO artists_songs (artist_id, song_id, group_member)
        VALUES (%s, %s, %s);
        ''',
    'get_all_artists': '''
        SELECT DISTINCT artists.id, artists.name FROM artists
        INNER JOIN artists_albums ON artists_albums.artist_id = artists.id
        ORDER BY artists.name;
        ''',
    'get_all_albums': '''
        SELECT DISTINCT albums.id, albums.name, artists.name
        FROM albums
        INNER JOIN artists_albums ON artists_albums.album_id = albums.id
        INNER JOIN artists ON artists.id = artists_albums.artist_id
        INNER JOIN songs ON songs.album_id = albums.id
        WHERE SINGLE = 0
        GROUP BY albums.id
        ORDER BY artists.producer ASC, artists.name, songs.DATE ASC;
        ''',
    'get_album_artists': '''
        SELECT artists.id, artists.name FROM artists
        INNER JOIN artists_albums ON artists_albums.artist_id = artists.id
        INNER JOIN albums ON albums.id = artists_albums.album_id
        WHERE album_id = %s
        ORDER BY artists.producer ASC, artists.name;
        ''',
    'get_artist_name': '''
        SELECT name FROM artists WHERE id = %s;
        ''',
    'get_artist_songs': '''
        SELECT songs.id, songs.name, albums.name, songs.length, albums.id
        FROM songs
        INNER JOIN albums ON albums.id = songs.album_id
        INNER JOIN artists_songs ON artists_songs.song_id = songs.id
        INNER JOIN artists ON artists.id = artists_songs.artist_id
        WHERE artists.id = %s AND songs.length > 1 AND albums.mixtape = 0
        ORDER BY songs.play_count DESC, songs.date DESC, songs.track_number ASC;
        ''',
    'get_song_artists': '''
        SELECT artists.id, artists.name FROM artists
        INNER JOIN artists_songs ON artists_songs.artist_id = artists.id
        INNER JOIN songs ON songs.id = artists_songs.song_id
        WHERE songs.id = %s AND artists_songs.group_member = 0
        ORDER BY artists_songs.id;
        ''',
    'get_artist_albums': '''
        SELECT DISTINCT albums.id, albums.name, artists.name FROM albums
        INNER JOIN artists_albums ON artists_albums.album_id = albums.id
        INNER JOIN artists ON artists.id = artists_albums.artist_id
        INNER JOIN songs ON songs.album_id = albums.id
        WHERE artists.id = %s AND albums.single = %s AND albums.mixtape = %s
        ORDER BY songs.date DESC;
        ''',
    'get_album_info': '''
        SELECT albums.name, albums.multi_disc, COUNT(songs.track_number), 
        SUM(songs.length), songs.date
        FROM albums
        INNER JOIN songs ON songs.album_id = albums.id
        WHERE albums.id = %s AND songs.bonus = 0
        ORDER BY songs.track_number;
        ''',
    'get_album_songs': '''
        SELECT id, track_number, name, length FROM songs
        WHERE album_id = %s AND bonus = 0
        ORDER BY track_number;
        ''',
    'get_album_bonus_songs': '''
        SELECT id, track_number, name, length FROM songs
        WHERE album_id = %s AND bonus = 1
        ORDER BY track_number;
        ''',
    'get_disc_info': '''
        SELECT DISTINCT id, name FROM discs
        WHERE album_id = %s
        ORDER BY disc_number; 
        ''',
    'get_songs_on_disc': '''
        SELECT id, track_number, name, length FROM songs
        WHERE disc_id = %s AND bonus = 0
        ORDER BY track_number;
        ''',
    'get_playlists': '''
        SELECT id, name FROM playlists ORDER BY name;
        ''',
    'insert_playlist': '''
        INSERT INTO playlists (name)
        VALUES (%s);
        ''',
    'insert_playlist_song_link': '''
        INSERT INTO playlists_songs (playlist_id, song_id)
        VALUES (%s, %s);
        ''',
    'get_playlist_name': '''
        SELECT name FROM playlists WHERE id = %s;
        ''',
    'get_playlist_songs': '''
        SELECT songs.id, songs.name, albums.name, songs.length, albums.id
        FROM songs
        INNER JOIN albums ON albums.id = songs.album_id
        INNER JOIN playlists_songs ON playlists_songs.song_id = songs.id
        INNER JOIN playlists ON playlists.id = playlists_songs.playlist_id
        WHERE playlists.id = %s
        ORDER BY playlists_songs.id ASC;
        ''',
    'delete_playlist': '''
        DELETE FROM playlists WHERE id = %s;
        ''',
    'delete_song_from_playlist': '''
        DELETE FROM playlists_songs
        WHERE playlist_id = %s AND song_id = %s;
        ''',
    'search_artists': '''
        SELECT id, name FROM artists
        WHERE name LIKE %s;
        ''',
    'search_albums': '''
        SELECT DISTINCT albums.id, albums.name, artists.name
        FROM albums
        INNER JOIN artists_albums ON artists_albums.album_id = albums.id
        INNER JOIN artists ON artists.id = artists_albums.artist_id
        INNER JOIN songs ON songs.album_id = albums.id
        WHERE albums.name LIKE %s
        GROUP BY albums.id;
        ''',
    'search_songs': '''
        SELECT DISTINCT songs.id, songs.name, albums.name, songs.length, 
        albums.id
        FROM songs
        INNER JOIN albums ON albums.id = songs.album_id
        INNER JOIN artists_songs ON artists_songs.song_id = songs.id
        INNER JOIN artists ON artists.id = artists_songs.artist_id
        WHERE songs.name LIKE %s;
        ''',
}
