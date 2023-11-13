database = {
    "artists": {
        "columns": ["name"],
        "queries": {
            "read": {
                "id": """SELECT id FROM artists WHERE name = ?""",
                "all": """SELECT id, name FROM artists WHERE id = ?""",
            },
            "write": """INSERT INTO artists (name) VALUES (?)""",
        },
    },
    "albums": {
        "columns": ["name", "release_date", "multidisc", "single"],
        "queries": {
            "read": {
                "id": """SELECT id FROM albums WHERE name = ? AND release_date = ?""",
                "all": """SELECT id, name, release_date, multidisc, single
                        FROM albums WHERE id = ?""",
            },
            "write": """INSERT INTO albums (name, release_date, multidisc, single)
                        VALUES (?, ?, ?, ?)""",
        },
    },
    "discs": {
        "columns": ["album_id", "name", "disc_number"],
        "queries": {
            "read": {
                "id": """SELECT id FROM discs WHERE album_id = ? AND disc_number = ?""",
                "all": """SELECT id, album_id, name, disc_number
                        FROM discs WHERE id = ?""",
            },
            "write": """INSERT INTO discs (album_id, name, disc_number)
                        VALUES (?, ?, ?)""",
        },
    },
    "songs": {
        "columns": ["album_id", "name", "track_number", "length", "path",
                    "source", "disc_id"],
        "queries": {
            "read": {
                "id": """SELECT id FROM songs WHERE path = ?""",
                "all": """SELECT id, album_id, disc_id, name, track_number,
                            length, path, source
                        FROM songs WHERE id = ?""",
            },
            "write": """INSERT INTO songs (album_id, name, track_number,
                            length, path, source, disc_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        },
    },
    "artists_albums": {
        "columns": ["artist_id", "album_id"],
        "queries": {
            "read": {
                "id": """SELECT id FROM artists_albums
                        WHERE artist_id = ? AND album_id = ?""",
                "all": """SELECT id, artist_id, album_id
                        FROM artists_albums WHERE id = ?""",
            },
            "write": """INSERT INTO artists_albums (artist_id, album_id)
                        VALUES (?, ?)""",
        },
    },
    "artists_songs": {
        "columns": ["artist_id", "song_id", "group_member"],
        "queries": {
            "read": {
                "id": """SELECT id FROM artists_songs
                        WHERE artist_id = ? AND song_id = ?""",
                "all": """SELECT id, artist_id, song_id, group_member
                        FROM artists_songs WHERE id = ?""",
            },
            "write": """INSERT INTO artists_songs (artist_id, song_id, group_member)
                        VALUES (?, ?, ?)""",
        },
    },
    "producers_songs": {
        "columns": ["artist_id", "song_id", "coproducer", "additional"],
        "queries": {
            "read": {
                "id": """SELECT id FROM producers_songs
                        WHERE artist_id = ? AND song_id = ?""",
                "all": """SELECT id, artist_id, song_id, coproducer, additional
                        FROM producers_songs WHERE id = ?""",
            },
            "write": """INSERT INTO producers_songs (artist_id, song_id,
                            coproducer, additional)
                        VALUES (?, ?, ?, ?)""",
        },
    },
    "playlists": {
        "columns": ["name"],
        "queries": {
            "read": {
                "id": """SELECT id FROM playlists WHERE name = ?""",
                "all": """SELECT id, name FROM playlists WHERE id = ?""",
            },
            "write": """INSERT INTO playlists (name) VALUES (?)""",
        },
    },
    "playlists_songs": {
        "columns": ["playlist_id", "song_id"],
        "queries": {
            "read": {
                "id": """SELECT id FROM playlists_songs
                        WHERE playlist_id = ? AND song_id = ?""",
                "all": """SELECT id, playlist_id, song_id
                        FROM playlists_songs WHERE id = ?""",
            },
            "write": """INSERT INTO playlists_songs (playlist_id, song_id)
                        VALUES (?, ?)""",
        },
    },
    "hubs": {
        "columns": ["name"],
        "queries": {
            "read": {
                "id": """SELECT id FROM hubs WHERE name = ?""",
                "all": """SELECT id, name FROM hubs WHERE id = ?""",
            },
            "write": """INSERT INTO hubs (name) VALUES (?)""",
        },
    },
    "hubs_albums": {
        "columns": ["hub_id", "album_id"],
        "queries": {
            "read": {
                "id": """SELECT id FROM hubs_albums
                        WHERE hub_id = ? AND album_id = ?""",
                "all": """SELECT id, hub_id, album_id
                        FROM hubs_albums WHERE id = ?""",
            },
            "write": """INSERT INTO hubs_albums (hub_id, album_id)
                        VALUES (?, ?)""",
        },
    },
}

required_metadata_input_fields = {
    "album": ["album_artists", "album", "release_date"],
    "song": ["title", "song_artists", "source"],
    "multidisc": ["disc_name", "disc_number"],
}
