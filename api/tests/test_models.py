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
