from tinytag import TinyTag


class Song:
    def __init__(self, path):
        song = TinyTag.get(path)

        self.album_artists = song.albumartist.split("; ")
        self.song_artists = song.artist.split("; ")

        if song.composer is not None:
            self.group_members = song.composer.split("; ")
        else:
            self.group_members = None

        self.album = song.album

        self.title = song.title
        self.release_date = song.year
        self.length = song.duration
        self.track_number = int(song.track)
        self.path = path

        self.bonus_track = False
        self.single = False
        self.mixtape = False
        self.multi_disc = False

        if song.genre is not None:
            if song.genre == "Bonus":
                self.bonus_track = True
            elif song.genre == "Single":
                self.single = True
            elif song.genre == "Mixtape":
                self.mixtape = True
            else:
                self.multi_disc = True
                self.disc_title = song.genre
                self.disc_number = int(song.disc)
