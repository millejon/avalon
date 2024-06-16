import datetime

from django.test import TestCase
from django.db import IntegrityError

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

        artists = [artist.name for artist in models.Artist.objects.all()]

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

        albums = [album.title for album in models.Album.objects.all()]
        expected_album_order = [
            "Me Against The World",
            "All Eyez On Me",
            "Tha Streetz Iz A Mutha",
        ]

        self.assertEqual(albums, expected_album_order)
