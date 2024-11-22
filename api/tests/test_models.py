import datetime

from django.test import TestCase
from django.db import IntegrityError

from api import models


class ArtistModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tupac = models.Artist.objects.create(name="2Pac", hometown="Oakland, CA")

    def test_artist_creation_successful(self):
        self.assertEqual(self.tupac.name, "2Pac")
        self.assertEqual(self.tupac.hometown, "Oakland, CA")

    def test_artist_creation_without_hometown_successful(self):
        snoop_dogg = models.Artist.objects.create(name="Snoop Dogg")

        self.assertEqual(snoop_dogg.name, "Snoop Dogg")
        self.assertEqual(snoop_dogg.hometown, "")

    def test_artist_name_max_length_is_100(self):
        max_length = self.tupac._meta.get_field("name").max_length

        self.assertEqual(max_length, 100)

    def test_artist_name_unique_constraint_is_true(self):
        unique_constraint = self.tupac._meta.get_field("name").unique

        self.assertTrue(unique_constraint)

    def test_artist_hometown_max_length_is_100(self):
        max_length = self.tupac._meta.get_field("hometown").max_length

        self.assertEqual(max_length, 100)

    def test_artist_hometown_can_be_blank(self):
        blank = self.tupac._meta.get_field("hometown").blank

        self.assertTrue(blank)

    def test_artist_str_method_returns_artist_name(self):
        self.assertEqual(str(self.tupac), "2Pac")

    def test_artist_get_url_method_returns_artist_api_resource_url(self):
        self.assertEqual(self.tupac.get_url(), f"/api/artists/{self.tupac.id}")

    def test_duplicate_artist_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Artist.objects.create(name="2Pac")

    def test_duplicate_artist_creation_case_insensitive_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Artist.objects.create(name="2pac")

    def test_artists_ordered_by_name(self):
        models.Artist.objects.create(name="Snoop Dogg", hometown="Long Beach, CA")
        models.Artist.objects.create(name="Dr. Dre", hometown="Compton, CA")
        artists = [str(artist) for artist in models.Artist.objects.all()]

        self.assertEqual(artists, ["2Pac", "Dr. Dre", "Snoop Dogg"])


class AlbumModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.all_eyez_on_me = models.Album.objects.create(
            title="All Eyez On Me",
            release_date=datetime.date(1996, 2, 13),
            label="Death Row Records",
            album_type="multidisc",
        )

    def test_album_creation_successful(self):
        self.assertEqual(self.all_eyez_on_me.title, "All Eyez On Me")
        self.assertEqual(self.all_eyez_on_me.release_date, datetime.date(1996, 2, 13))
        self.assertEqual(self.all_eyez_on_me.label, "Death Row Records")
        self.assertEqual(self.all_eyez_on_me.album_type, "multidisc")

    def test_album_creation_without_label_successful(self):
        doggystyle = models.Album.objects.create(
            title="Doggystyle",
            release_date=datetime.date(1993, 11, 23),
            album_type="album",
        )

        self.assertEqual(doggystyle.title, "Doggystyle")
        self.assertEqual(doggystyle.release_date, datetime.date(1993, 11, 23))
        self.assertEqual(doggystyle.label, "")
        self.assertEqual(doggystyle.album_type, "album")

    def test_album_creation_album_type_album_by_default(self):
        the_chronic = models.Album.objects.create(
            title="The Chronic", release_date=datetime.date(1992, 12, 15)
        )

        self.assertEqual(the_chronic.title, "The Chronic")
        self.assertEqual(the_chronic.release_date, datetime.date(1992, 12, 15))
        self.assertEqual(the_chronic.album_type, "album")

    def test_album_title_max_length_is_600(self):
        max_length = self.all_eyez_on_me._meta.get_field("title").max_length

        self.assertEqual(max_length, 600)

    def test_album_artists_related_name_is_album_artists(self):
        related_name = self.all_eyez_on_me._meta.get_field("artists")._related_name

        self.assertEqual(related_name, "album_artists")

    def test_album_label_max_length_is_100(self):
        max_length = self.all_eyez_on_me._meta.get_field("label").max_length

        self.assertEqual(max_length, 100)

    def test_album_label_can_be_blank(self):
        blank = self.all_eyez_on_me._meta.get_field("label").blank

        self.assertTrue(blank)

    def test_album_album_type_max_length_is_10(self):
        max_length = self.all_eyez_on_me._meta.get_field("album_type").max_length

        self.assertEqual(max_length, 10)

    def test_album_album_type_has_three_choices(self):
        album_types = [
            ("album", "album"),
            ("multidisc", "multidisc"),
            ("single", "single"),
        ]
        type_choices = self.all_eyez_on_me._meta.get_field("album_type").choices

        self.assertEqual(album_types, type_choices)

    def test_album_str_method_returns_album_title(self):
        self.assertEqual(str(self.all_eyez_on_me), "All Eyez On Me")

    def test_duplicate_album_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Album.objects.create(
                title="All Eyez On Me",
                release_date=datetime.date(1996, 2, 13),
                label="Death Row Records",
                album_type="multidisc",
            )

    def test_duplicate_album_creation_case_insensitive_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Album.objects.create(
                title="all eyez on me",
                release_date=datetime.date(1996, 2, 13),
                album_type="album",
            )

    def test_albums_ordered_by_release_date(self):
        models.Album.objects.create(
            title="Necessary Roughness",
            release_date=datetime.date(1997, 6, 24),
            label="Death Row Records",
            album_type="album",
        )
        models.Album.objects.create(
            title="Dogg Food",
            release_date=datetime.date(1995, 10, 31),
            label="Death Row Records",
            album_type="album",
        )
        albums = [str(album) for album in models.Album.objects.all()]

        self.assertEqual(albums, ["Dogg Food", "All Eyez On Me", "Necessary Roughness"])


class AlbumArtistModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.kurupt = models.Artist.objects.create(
            name="Kurupt", hometown="Los Angeles, CA"
        )
        cls.dogg_food = models.Album.objects.create(
            title="Dogg Food",
            release_date=datetime.date(1995, 10, 31),
            label="Death Row Records",
            album_type="album",
        )
        cls.album_artist_link = models.AlbumArtist.objects.create(
            album=cls.dogg_food, artist=cls.kurupt
        )

    def test_album_artist_creation_successful(self):
        self.assertEqual(self.album_artist_link.album.title, "Dogg Food")
        self.assertEqual(self.album_artist_link.artist.name, "Kurupt")

    def test_album_artist_str_method_returns_artist_name_album_title(self):
        self.assertEqual(str(self.album_artist_link), "Kurupt - Dogg Food")

    def test_duplicate_album_artist_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.AlbumArtist.objects.create(album=self.dogg_food, artist=self.kurupt)

    def test_album_artists_ordered_by_album_artist_id(self):
        tha_dogg_pound = models.Artist.objects.create(
            name="Tha Dogg Pound", hometown="Los Angeles, CA"
        )
        daz_dillinger = models.Artist.objects.create(
            name="Daz Dillinger", hometown="Long Beach, CA"
        )
        models.AlbumArtist.objects.create(album=self.dogg_food, artist=tha_dogg_pound)
        models.AlbumArtist.objects.create(album=self.dogg_food, artist=daz_dillinger)
        album_artists = [str(artist) for artist in models.AlbumArtist.objects.all()]

        self.assertEqual(
            album_artists,
            [
                "Kurupt - Dogg Food",
                "Tha Dogg Pound - Dogg Food",
                "Daz Dillinger - Dogg Food",
            ],
        )
