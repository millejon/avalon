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

    def test_artist_creation_without_optional_fields_successful(self):
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
