database = {
    "artists": {
        "columns": ["name"],
        "queries": {
            "read": {
                "id": """SELECT id FROM artists WHERE name = ?""",
                "all": """SELECT name FROM artists WHERE id = ?""",
                "all_artists": """
                    SELECT DISTINCT artists.id FROM artists
                    INNER JOIN artists_albums on artists.id = artists_albums.artist_id
                    INNER JOIN albums on artists_albums.album_id = albums.id
                    WHERE albums.single = 0
                    ORDER BY artists.name
                """,
            },
            "write": {
                "add": """INSERT INTO artists (name) VALUES (?)""",
            },
        },
    },
    "albums": {
        "columns": ["title", "release_date", "multidisc", "single"],
        "queries": {
            "read": {
                "id": """SELECT id FROM albums WHERE title = ? AND release_date = ?""",
                "all": """
                    SELECT title, release_date, multidisc, single
                    FROM albums WHERE id = ?
                """,
                "length": """
                    SELECT SUM(songs.length) FROM songs
                    INNER JOIN albums ON songs.album_id = albums.id
                    WHERE albums.id = ?
                """,
                "all_albums": """
                    SELECT DISTINCT albums.id FROM albums
                    INNER JOIN artists_albums on albums.id = artists_albums.album_id
                    INNER JOIN artists on artists_albums.artist_id = artists.id
                    WHERE albums.single = 0
                    ORDER BY artists.name, albums.release_date
                """,
            },
            "write": {
                "add": """
                    INSERT INTO albums (title, release_date, multidisc, single)
                    VALUES (?, ?, ?, ?)
                """,
            },
        },
    },
    "discs": {
        "columns": ["album_id", "title", "disc_number"],
        "queries": {
            "read": {
                "id": """SELECT id FROM discs WHERE album_id = ? AND disc_number = ?""",
                "all": """
                    SELECT album_id, title, disc_number
                    FROM discs WHERE id = ?
                """,
            },
            "write": {
                "add": """
                    INSERT INTO discs (album_id, title, disc_number)
                    VALUES (?, ?, ?)
                """,
            },
        },
    },
    "songs": {
        "columns": [
            "album_id",
            "disc_id",
            "title",
            "track_number",
            "length",
            "path",
            "comment",
            "source",
        ],
        "queries": {
            "read": {
                "id": """SELECT id FROM songs WHERE path = ?""",
                "all": """
                    SELECT album_id, disc_id, title, track_number, length,
                        path, source, comment
                    FROM songs WHERE id = ?
                """,
                "album": """SELECT id FROM songs WHERE album_id = ?""",
            },
            "write": {
                "add": """
                    INSERT INTO songs (album_id, disc_id, title, track_number,
                        length, path, comment, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
            },
        },
    },
    "artists_albums": {
        "columns": ["artist_id", "album_id"],
        "queries": {
            "read": {
                "id": """
                    SELECT id FROM artists_albums
                    WHERE artist_id = ? AND album_id = ?
                """,
                "all": """
                    SELECT artist_id, album_id
                    FROM artists_albums WHERE id = ?
                """,
                "albums": """
                    SELECT albums.id FROM albums
                    INNER JOIN artists_albums ON albums.id = artists_albums.album_id
                    WHERE artists_albums.artist_id = ? AND albums.single = 0
                    ORDER BY albums.release_date DESC
                """,
                "singles": """
                    SELECT albums.id FROM albums
                    INNER JOIN artists_albums ON albums.id = artists_albums.album_id
                    WHERE artists_albums.artist_id = ? AND albums.single = 1
                    ORDER BY albums.release_date DESC
                """,
                "artists": """
                    SELECT artists.id, artists.name FROM artists
                    INNER JOIN artists_albums ON artists.id = artists_albums.artist_id
                    WHERE artists_albums.album_id = ?
                """,
            },
            "write": {
                "add": """
                    INSERT INTO artists_albums (artist_id, album_id)
                    VALUES (?, ?)
                """,
            },
        },
    },
    "artists_songs": {
        "columns": ["artist_id", "song_id", "group_member"],
        "queries": {
            "read": {
                "id": """
                    SELECT id FROM artists_songs
                    WHERE artist_id = ? AND song_id = ?
                """,
                "all": """
                    SELECT artist_id, song_id, group_member
                    FROM artists_songs WHERE id = ?
                """,
                "songs": """
                    SELECT songs.id FROM songs
                    INNER JOIN artists_songs ON songs.id = artists_songs.song_id
                    INNER JOIN albums on songs.album_id = albums.id
                    WHERE artists_songs.artist_id = ? AND songs.length > 1
                    ORDER BY songs.play_count DESC, albums.release_date DESC
                """,
                "artists": """
                    SELECT artists.id, artists.name FROM artists
                    INNER JOIN artists_songs ON artists.id = artists_songs.artist_id
                    WHERE artists_songs.song_id = ? AND artists_songs.group_member = 0
                """,
            },
            "write": {
                "add": """
                    INSERT INTO artists_songs (artist_id, song_id, group_member)
                    VALUES (?, ?, ?)
                """,
            },
        },
    },
    "producers_songs": {
        "columns": ["artist_id", "song_id", "coproducer", "additional"],
        "queries": {
            "read": {
                "id": """
                    SELECT id FROM producers_songs
                    WHERE artist_id = ? AND song_id = ?
                """,
                "all": """
                    SELECT artist_id, song_id, coproducer, additional
                    FROM producers_songs WHERE id = ?
                """,
                "songs": """
                    SELECT songs.id, producers_songs.coproducer, producers_songs.additional
                    FROM SONGS
                    INNER JOIN producers_songs ON songs.id = producers_songs.song_id
                    INNER JOIN albums on songs.album_id = albums.id
                    WHERE producers_songs.artist_id = ? AND songs.length > 1
                    ORDER BY songs.play_count DESC, albums.release_date DESC
                """,
                "producers": """
                    SELECT artists.id, artists.name FROM artists
                    INNER JOIN producers_songs ON artists.id = producers_songs.artist_id
                    WHERE producers_songs.song_id = ?
                        AND producers_songs.coproducer = 0
                        AND producers_songs.additional = 0
                """,
            },
            "write": {
                "add": """
                    INSERT INTO producers_songs (artist_id, song_id, coproducer, additional)
                    VALUES (?, ?, ?, ?)
                """,
            },
        },
    },
    "playlists": {
        "columns": ["title"],
        "queries": {
            "read": {
                "id": """SELECT id FROM playlists WHERE title = ?""",
                "all": """SELECT title FROM playlists WHERE id = ?""",
                "all_playlists": """SELECT id FROM playlists""",
            },
            "write": {
                "add": """INSERT INTO playlists (title) VALUES (?)""",
            },
        },
    },
    "playlists_songs": {
        "columns": ["playlist_id", "song_id"],
        "queries": {
            "read": {
                "id": """
                    SELECT id FROM playlists_songs
                    WHERE playlist_id = ? AND song_id = ?
                """,
                "all": """
                    SELECT playlist_id, song_id
                    FROM playlists_songs WHERE id = ?
                """,
                "songs": """
                    SELECT songs.id FROM songs
                    INNER JOIN playlists_songs ON songs.id = playlists_songs.song_id
                    INNER JOIN albums on songs.album_id = albums.id
                    WHERE playlists_songs.playlist_id = ?
                    ORDER BY playlists_songs.id
                """,
            },
            "write": {
                "add": """
                    INSERT INTO playlists_songs (playlist_id, song_id)
                    VALUES (?, ?)
                """,
                "delete": """
                    DELETE FROM playlists_songs
                    WHERE playlist_id = ? AND song_id = ?
                """,
            },
        },
    },
    "hubs": {
        "columns": ["name"],
        "queries": {
            "read": {
                "id": """SELECT id FROM hubs WHERE name = ?""",
                "all": """SELECT name FROM hubs WHERE id = ?""",
                "all_hubs": """SELECT id FROM hubs ORDER BY name""",
            },
            "write": {
                "add": """INSERT INTO hubs (name) VALUES (?)""",
            },
        },
    },
    "hubs_albums": {
        "columns": ["hub_id", "album_id"],
        "queries": {
            "read": {
                "id": """
                    SELECT id FROM hubs_albums
                    WHERE hub_id = ? AND album_id = ?
                """,
                "all": """
                    SELECT hub_id, album_id FROM hubs_albums
                    WHERE id = ?
                """,
                "albums": """
                    SELECT hubs_albums.album_id FROM hubs_albums
                    INNER JOIN albums ON hubs_albums.album_id = albums.id
                    WHERE hubs_albums.hub_id = ?
                    ORDER BY albums.release_date DESC
                """,
                "songs": """
                    SELECT songs.id FROM songs
                    INNER JOIN albums ON songs.album_id = albums.id
                    INNER JOIN hubs_albums ON albums.id = hubs_albums.album_id
                    WHERE hubs_albums.hub_id = ?
                    ORDER BY songs.play_count DESC, albums.release_date DESC
                """,
            },
            "write": {
                "add": """
                    INSERT INTO hubs_albums (hub_id, album_id)
                    VALUES (?, ?)
                """,
            },
        },
    },
}

required_metadata_input_fields = {
    "album": ["album_artists", "album", "release_date"],
    "song": ["title", "song_artists", "source"],
    "multidisc": ["disc_title", "disc_number"],
}

punctuation_replacements = {
    "+": "and",
    "&": "and",
    "#": "number",
    "=": "equals",
}

metadata_modifications = {
    "lists": [
        "album_artists",
        "hubs",
        "song_artists",
        "group_members",
        "producers",
        "coproducers",
        "additional_producers",
    ],
    "integers": ["track_number", "disc_number"],
    "bools": ["single", "multidisc"],
}
