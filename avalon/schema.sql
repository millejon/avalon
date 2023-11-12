DROP TABLE IF EXISTS hubs_albums;
DROP TABLE IF EXISTS hubs;
DROP TABLE IF EXISTS playlists_songs;
DROP TABLE IF EXISTS playlists;
DROP TABLE IF EXISTS artists_songs;
DROP TABLE IF EXISTS producers_songs;
DROP TABLE IF EXISTS artists_albums;
DROP TABLE IF EXISTS discs;
DROP TABLE IF EXISTS songs;
DROP TABLE IF EXISTS albums;
DROP TABLE IF EXISTS artists;

CREATE TABLE artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE albums (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    release_date TEXT NOT NULL,
    multidisc INTEGER DEFAULT FALSE,
    single INTEGER DEFAULT FALSE,
    UNIQUE (name, release_date)
);

CREATE TABLE discs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    album_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    disc_number INTEGER NOT NULL,
    FOREIGN KEY (album_id) REFERENCES albums (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    UNIQUE (album_id, disc_number)
);

CREATE TABLE songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    album_id INTEGER NOT NULL,
    disc_id INTEGER,
    name TEXT NOT NULL,
    track_number INTEGER NOT NULL,
    length INTEGER NOT NULL,
    path TEXT UNIQUE NOT NULL,
    source TEXT NOT NULL,
    play_count INTEGER DEFAULT 0,
    FOREIGN KEY (album_id) REFERENCES albums (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    FOREIGN KEY (disc_id) REFERENCES discs (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);

CREATE TABLE artists_albums (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_id INTEGER NOT NULL,
    album_id INTEGER NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artists (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    FOREIGN KEY (album_id) REFERENCES albums (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    UNIQUE (artist_id, album_id)
);

CREATE TABLE artists_songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_id INTEGER NOT NULL,
    song_id INTEGER NOT NULL,
    group_member INTEGER DEFAULT FALSE,
    FOREIGN KEY (artist_id) REFERENCES artists (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    FOREIGN KEY (song_id) REFERENCES songs (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    UNIQUE (artist_id, song_id)
);

CREATE TABLE producers_songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_id INTEGER NOT NULL,
    song_id INTEGER NOT NULL,
    coproducer INTEGER DEFAULT FALSE,
    additional INTEGER DEFAULT FALSE,
    FOREIGN KEY (artist_id) REFERENCES artists (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    FOREIGN KEY (song_id) REFERENCES songs (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    UNIQUE (artist_id, song_id)
);

CREATE TABLE playlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE playlists_songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    playlist_id INTEGER NOT NULL,
    song_id INTEGER NOT NULL,
    FOREIGN KEY (playlist_id) REFERENCES playlists (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    FOREIGN KEY (song_id) REFERENCES songs (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    UNIQUE (playlist_id, song_id)
);

CREATE TABLE hubs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE hubs_albums (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hub_id INTEGER NOT NULL,
    album_id INTEGER NOT NULL,
    FOREIGN KEY (hub_id) REFERENCES hubs (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    FOREIGN KEY (album_id) REFERENCES albums (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION,
    UNIQUE (hub_id, album_id)
);
