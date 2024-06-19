import datetime

from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone

from api import models


class ArtistModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.artist = models.Artist.objects.create(name="2pac")

    def test_artist_creation(self):
        self.assertEqual(self.artist.name, "2pac")

    def test_name_max_length(self):
        max_length = self.artist._meta.get_field("name").max_length

        self.assertEqual(max_length, 100)

    def test_artist_str_method(self):
        self.assertEqual(str(self.artist), "2pac")

    def test_artist_get_absolute_url(self):
        # TODO: Add test after coding front-end views
        pass

    def test_nonunique_artist_creation(self):
        with self.assertRaises(IntegrityError):
            models.Artist.objects.create(name="2pac")

    def test_nonunique_artist_creation_case_insensitive(self):
        with self.assertRaises(IntegrityError):
            models.Artist.objects.create(name="2Pac")

    def test_artist_ordering(self):
        models.Artist.objects.create(name="Xzibit")
        models.Artist.objects.create(name="Kurupt")

        artists = [str(artist) for artist in models.Artist.objects.all()]

        self.assertEqual(artists, ["2pac", "Kurupt", "Xzibit"])


class AlbumModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.artist = models.Artist.objects.create(name="2pac")
        cls.album = models.Album.objects.create(
            title="Me Against The World",
            release_date=datetime.date(1995, 3, 14),
        )
        cls.album.artists.add(cls.artist)

    def test_album_creation(self):
        self.assertTrue(self.album.artists.contains(self.artist))
        self.assertEqual(self.album.title, "Me Against The World")
        self.assertEqual(self.album.release_date, datetime.date(1995, 3, 14))

    def test_album_creation_single_false_by_default(self):
        self.assertFalse(self.album.single)

    def test_album_creation_multidisc_false_by_default(self):
        self.assertFalse(self.album.multidisc)

    def test_title_max_length(self):
        max_length = self.album._meta.get_field("title").max_length

        self.assertEqual(max_length, 600)

    def test_album_str_method(self):
        self.assertEqual(str(self.album), "Me Against The World")

    def test_album_get_absolute_url(self):
        # TODO: Add test after coding front-end views
        pass

    def test_nonunique_album_creation(self):
        with self.assertRaises(IntegrityError):
            models.Album.objects.create(
                title="Me Against The World",
                release_date=datetime.date(1995, 3, 14),
            )

    def test_album_ordering(self):
        artist2 = models.Artist.objects.create(name="Kurupt")
        album2 = models.Album.objects.create(
            title="Tha Streetz Iz A Mutha",
            release_date=datetime.date(1999, 11, 16),
        )
        album2.artists.add(artist2)
        album3 = models.Album.objects.create(
            title="All Eyez On Me",
            release_date=datetime.date(1996, 2, 13),
            multidisc=True,
        )
        album3.artists.add(self.artist)

        albums = [str(album) for album in models.Album.objects.all()]
        expected_album_order = [
            "Me Against The World",
            "All Eyez On Me",
            "Tha Streetz Iz A Mutha",
        ]

        self.assertEqual(albums, expected_album_order)


class DiscModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.artist = models.Artist.objects.create(name="2pac")
        cls.album = models.Album.objects.create(
            title="All Eyez On Me",
            release_date=datetime.date(1996, 2, 13),
            multidisc=True,
        )
        cls.album.artists.add(cls.artist)
        cls.disc = models.Disc.objects.create(
            album=cls.album,
            title="Book 2",
            number=2,
        )

    def test_disc_creation(self):
        self.assertEqual(self.disc.album.title, "All Eyez On Me")
        self.assertEqual(self.disc.title, "Book 2")
        self.assertEqual(self.disc.number, 2)

    def test_title_max_length(self):
        max_length = self.disc._meta.get_field("title").max_length

        self.assertEqual(max_length, 100)

    def test_disc_str_method(self):
        self.assertEqual(str(self.disc), "All Eyez On Me (Book 2)")

    def test_nonunique_disc_creation(self):
        with self.assertRaises(IntegrityError):
            models.Disc.objects.create(
                album=self.album,
                title="Book 2",
                number=2,
            )

    def test_invalid_disc_number_disc_creation(self):
        with self.assertRaises(IntegrityError):
            models.Disc.objects.create(
                album=self.album,
                title="Book 0",
                number=0,
            )

    def test_disc_ordering(self):
        artist2 = models.Artist.objects.create(name="Wu-Tang Clan")
        album2 = models.Album.objects.create(
            title="Wu-Tang Forever",
            release_date=datetime.date(1997, 6, 3),
            multidisc=True,
        )
        album2.artists.add(artist2)
        models.Disc.objects.create(album=album2, title="Disc 1", number=1)
        album3 = models.Album.objects.create(
            title="R U Still Down? (Remember Me)",
            release_date=datetime.date(1997, 11, 25),
            multidisc=True,
        )
        album3.artists.add(self.artist)
        models.Disc.objects.create(album=album3, title="Disc Two", number=2)
        models.Disc.objects.create(album=self.album, title="Book 1", number=1)

        discs = [str(disc) for disc in models.Disc.objects.all()]
        expected_disc_order = [
            "All Eyez On Me (Book 1)",
            "All Eyez On Me (Book 2)",
            "R U Still Down? (Remember Me) (Disc Two)",
            "Wu-Tang Forever (Disc 1)",
        ]

        self.assertEqual(discs, expected_disc_order)


class SongModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.artist = models.Artist.objects.create(name="Nas")
        cls.album = models.Album.objects.create(
            title="Illmatic",
            release_date=datetime.date(1994, 4, 19),
        )
        cls.album.artists.add(cls.artist)
        cls.song = models.Song.objects.create(
            album=cls.album,
            title="Life's A Bitch",
            track_number=3,
            length=210,
            path="D:/Music/nas/illmatic/03_lifes_a_bitch.flac",
        )
        cls.song.artists.add(cls.artist)

    def test_song_creation(self):
        self.assertTrue(self.song.artists.contains(self.artist))
        self.assertEqual(self.song.album, self.album)
        self.assertEqual(self.song.title, "Life's A Bitch")
        self.assertEqual(self.song.track_number, 3)
        self.assertEqual(self.song.length, 210)
        self.assertEqual(self.song.path, "D:/Music/nas/illmatic/03_lifes_a_bitch.flac")

    def test_song_creation_disc_null_by_default(self):
        self.assertIsNone(self.song.disc)

    def test_song_creation_play_count_zero_by_default(self):
        self.assertEqual(self.song.play_count, 0)

    def test_title_max_length(self):
        max_length = self.song._meta.get_field("title").max_length

        self.assertEqual(max_length, 600)

    def test_path_max_length(self):
        max_length = self.song._meta.get_field("path").max_length

        self.assertEqual(max_length, 1000)

    def test_song_str_method(self):
        self.assertEqual(str(self.song), "3. Life's A Bitch [Illmatic]")

    def test_nonunique_song_creation(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                album=self.album,
                title="Life's a Bitch",
                track_number=3,
                length=212,
                path="D:/Music/nas/illmatic/03_lifes_a_bitch.flac",
            )

    def test_invalid_song_track_number_song_creation(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                album=self.album,
                title="N.Y. State Of Mind",
                track_number=0,
                length=293,
                path="D:/Music/nas/illmatic/00_ny_state_of_mind.flac",
            )

    def test_song_ordering(self):
        album2 = models.Album.objects.create(
            title="Street's Disciple",
            release_date=datetime.date(2004, 11, 30),
        )
        disc1 = models.Disc.objects.create(album=album2, title="Disc 1", number=1)
        disc2 = models.Disc.objects.create(album=album2, title="Disc 2", number=2)
        models.Song.objects.create(
            album=album2,
            disc=disc2,
            title="Suicide Bounce",
            track_number=1,
            length=237,
            path="D:/Music/nas/streets-disciple/disc-2/01_suicide_bounce.flac",
        )
        models.Song.objects.create(
            album=album2,
            disc=disc1,
            title="Just A Moment",
            track_number=10,
            length=263,
            path="D:/Music/nas/streets-disciple/disc-1/10_just_a_moment.flac",
        )

        songs = [str(song) for song in models.Song.objects.all()]
        expected_song_order = [
            "10. Just A Moment [Street's Disciple]",
            "1. Suicide Bounce [Street's Disciple]",
            "3. Life's A Bitch [Illmatic]",
        ]

        self.assertEqual(songs, expected_song_order)


class FeatureModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.artist = models.Artist.objects.create(name="Kurupt")
        cls.album = models.Album.objects.create(
            title="Tha Streetz Iz A Mutha", release_date=datetime.date(1999, 11, 16)
        )
        cls.song = models.Song.objects.create(
            album=cls.album,
            title="Who Ride Wit Us",
            track_number=3,
            length=261,
            path="D:/Music/kurupt/tha-streetz-iz-a-mutha/03_who_ride_wit_us.flac",
        )
        cls.feature = models.Feature.objects.create(artist=cls.artist, song=cls.song)

    def test_feature_creation(self):
        self.assertEqual(self.feature.artist.name, "Kurupt")
        self.assertEqual(self.feature.song.title, "Who Ride Wit Us")

    def test_feature_creation_group_false_by_default(self):
        self.assertFalse(self.feature.group)

    def test_feature_creation_producer_false_by_default(self):
        self.assertFalse(self.feature.producer)

    def test_feature_creation_producer_role_empty_string_by_default(self):
        self.assertEqual(self.feature.role, "")

    def test_role_max_length(self):
        max_length = self.feature._meta.get_field("role").max_length

        self.assertEqual(max_length, 100)

    def test_nonunique_feature_creation(self):
        with self.assertRaises(IntegrityError):
            models.Feature.objects.create(artist=self.artist, song=self.song)

    def test_group_member_creation(self):
        group = models.Artist.objects.create(name="Tha Dogg Pound")
        group_feature = models.Feature.objects.create(
            artist=group, song=self.song, group=True
        )

        self.assertEqual(group_feature.artist.name, "Tha Dogg Pound")
        self.assertEqual(group_feature.song.title, "Who Ride Wit Us")
        self.assertTrue(group_feature.group)

    def test_nonunique_group_member_creation(self):
        group = models.Artist.objects.create(name="Tha Dogg Pound")
        models.Feature.objects.create(artist=group, song=self.song, group=True)

        with self.assertRaises(IntegrityError):
            models.Feature.objects.create(artist=group, song=self.song, group=True)

    def test_producer_creation(self):
        producer = models.Artist.objects.create(name="Fredwreck")
        producer_feature = models.Feature.objects.create(
            artist=producer, song=self.song, producer=True, role="Producer"
        )

        self.assertEqual(producer_feature.artist.name, "Fredwreck")
        self.assertEqual(producer_feature.song.title, "Who Ride Wit Us")
        self.assertTrue(producer_feature.producer)
        self.assertEqual(producer_feature.role, "Producer")

    def test_nonunique_producer_creation(self):
        producer = models.Artist.objects.create(name="Fredwreck")
        models.Feature.objects.create(
            artist=producer, song=self.song, producer=True, role="Producer"
        )

        with self.assertRaises(IntegrityError):
            models.Feature.objects.create(
                artist=producer, song=self.song, producer=True, role="Producer"
            )


class PlaylistModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.playlist = models.Playlist.objects.create(title="Rock The Bells")

    def test_playlist_creation(self):
        self.assertEqual(self.playlist.title, "Rock The Bells")
        self.assertIsNotNone(self.playlist.created)
        self.assertIsNotNone(self.playlist.last_modified)
        self.assertEqual(self.playlist.created, self.playlist.last_modified)

    def test_playlist_creation_songs_null_by_default(self):
        self.assertEqual(self.playlist.songs.count(), 0)

    def test_title_max_length(self):
        max_length = self.playlist._meta.get_field("title").max_length

        self.assertEqual(max_length, 300)

    def test_playlist_str_method(self):
        self.assertEqual(str(self.playlist), "Rock The Bells")

    def test_playlist_get_absolute_url(self):
        # TODO: Add test after coding front-end views
        pass

    def test_nonunique_playlist_creation(self):
        with self.assertRaises(IntegrityError):
            models.Playlist.objects.create(title="Rock The Bells")

    def test_nonunique_playlist_creation_case_insensitive(self):
        with self.assertRaises(IntegrityError):
            models.Playlist.objects.create(title="rock the bells")

    def test_playlist_ordering(self):
        playlist2 = models.Playlist.objects.create(title="Kaleidoscope Dreams")
        models.Playlist.objects.create(title="Computer Love")
        album = models.Album.objects.create(
            title="Ready To Die", release_date=datetime.date(1994, 9, 13)
        )
        song = models.Song.objects.create(
            album=album,
            title="Machine Gun Funk",
            track_number=4,
            length=257,
            path="D:/Music/the-notorious-big/ready-to-die/04_machine_gun_funk.flac",
        )
        playlist2.songs.add(song)

        playlists = [str(playlist) for playlist in models.Playlist.objects.all()]

        self.assertEqual(
            playlists, ["Kaleidoscope Dreams", "Computer Love", "Rock The Bells"]
        )
