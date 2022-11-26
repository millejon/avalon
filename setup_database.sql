-- Drop any existing tables that will conflict with the new tables.
DROP TABLE IF EXISTS `artists_albums`;
DROP TABLE IF EXISTS `artists_songs`;
DROP TABLE IF EXISTS `playlists_songs`;
DROP TABLE IF EXISTS `songs`;
DROP TABLE IF EXISTS `artists`;
DROP TABLE IF EXISTS `discs`;
DROP TABLE IF EXISTS `albums`;
DROP TABLE IF EXISTS `playlists`;

CREATE TABLE artists (
    id INT AUTO_INCREMENT NOT NULL,
    name VARCHAR(255) UNIQUE NOT NULL,
    producer BOOLEAN DEFAULT 0,
    PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE albums (
    id INT AUTO_INCREMENT NOT NULL,
    name VARCHAR(255) NOT NULL,
    single BOOLEAN DEFAULT 0,
    mixtape BOOLEAN DEFAULT 0,
    multi_disc BOOLEAN DEFAULT 0,
    PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE discs (
    id INT AUTO_INCREMENT NOT NULL,
    album_id INT NOT NULL,
    disc_number INT(1) NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY album_disc(album_id, disc_number),
    FOREIGN KEY fk_album_disc(album_id) REFERENCES albums(id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE artists_albums (
    id INT AUTO_INCREMENT NOT NULL,
    artist_id INT NOT NULL,
    album_id INT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY artist_album(artist_id, album_id),
    FOREIGN KEY fk_artist_album(artist_id) REFERENCES artists(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY fk_album_artist(album_id) REFERENCES albums(id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE songs (
    id INT AUTO_INCREMENT NOT NULL,
    album_id INT NOT NULL,
    disc_id INT,
    track_number INT(2),
    name VARCHAR(255) NOT NULL,
    length INT NOT NULL,
    date DATE NOT NULL,
    path VARCHAR(255) UNIQUE NOT NULL,
    bonus BOOLEAN DEFAULT 0,
    play_count INT DEFAULT 0,
    PRIMARY KEY (id),
    FOREIGN KEY fk_album_song(album_id) REFERENCES albums(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY fk_disc_song(disc_id) REFERENCES discs(id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE artists_songs (
    id INT AUTO_INCREMENT NOT NULL,
    artist_id INT NOT NULL,
    song_id INT NOT NULL,
    group_member BOOLEAN,
    PRIMARY KEY (id),
    UNIQUE KEY artist_song(artist_id, song_id),
    FOREIGN KEY fk_artist_song(artist_id) REFERENCES artists(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY fk_song_artist(song_id) REFERENCES songs(id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE playlists (
    id INT AUTO_INCREMENT NOT NULL,
    name VARCHAR(255) UNIQUE NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE playlists_songs (
    id INT AUTO_INCREMENT NOT NULL,
    playlist_id INT NOT NULL,
    song_id INT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY playlist_song(playlist_id, song_id),
    FOREIGN KEY fk_playlist_song(playlist_id) REFERENCES playlists(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY fk_song_playlist(song_id) REFERENCES songs(id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

ALTER TABLE albums CONVERT TO CHARACTER SET utf8 COLLATE UTF8_GENERAL_CI;
ALTER TABLE artists CONVERT TO CHARACTER SET utf8 COLLATE UTF8_GENERAL_CI;
ALTER TABLE artists_albums CONVERT TO CHARACTER SET utf8 COLLATE UTF8_GENERAL_CI;
ALTER TABLE artists_songs CONVERT TO CHARACTER SET utf8 COLLATE UTF8_GENERAL_CI;
ALTER TABLE discs CONVERT TO CHARACTER SET utf8 COLLATE UTF8_GENERAL_CI;
ALTER TABLE playlists CONVERT TO CHARACTER SET utf8 COLLATE UTF8_GENERAL_CI;
ALTER TABLE playlists_songs CONVERT TO CHARACTER SET utf8 COLLATE UTF8_GENERAL_CI;
ALTER TABLE songs CONVERT TO CHARACTER SET utf8 COLLATE UTF8_GENERAL_CI;
