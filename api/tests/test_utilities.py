from django.test import TestCase

from api import models, utilities as util


class GetArtistsTestCase(TestCase):
    def test_get_artist_if_artist_in_database(self):
        mannie_fresh = models.Artist.objects.create(
            name="Mannie Fresh", hometown="New Orleans, LA"
        )
        album_artists = [{"name": "Mannie Fresh", "hometown": "New Orleans, LA"}]
        artists = util.get_artists(album_artists)

        self.assertEqual(artists, [mannie_fresh])

    def test_get_artist_if_artist_in_database_with_extraneous_whitespace(self):
        mannie_fresh = models.Artist.objects.create(
            name="Mannie Fresh", hometown="New Orleans, LA"
        )
        album_artists = [
            {"name": " Mannie  Fresh   ", "hometown": "   New    Orleans,  LA  "}
        ]
        artists = util.get_artists(album_artists)

        self.assertEqual(artists, [mannie_fresh])

    def test_create_artist_if_artist_not_in_database(self):
        album_artists = [{"name": "Birdman", "hometown": "New Orleans, LA"}]
        artists = util.get_artists(album_artists)
        birdman = models.Artist.objects.get(pk=artists[0].id)

        self.assertEqual(birdman.name, "Birdman")
        self.assertEqual(birdman.hometown, "New Orleans, LA")

    def test_create_artist_if_artist_not_in_database_with_extraneous_whitespace(self):
        album_artists = [{"name": "  Birdman ", "hometown": " New   Orleans,    LA  "}]
        artists = util.get_artists(album_artists)
        birdman = models.Artist.objects.get(pk=artists[0].id)

        self.assertEqual(birdman.name, "Birdman")
        self.assertEqual(birdman.hometown, "New Orleans, LA")

    def test_update_artist_if_hometown_is_submitted(self):
        big_tymers = models.Artist.objects.create(name="Big Tymers")
        album_artists = [{"name": "Big Tymers", "hometown": "New Orleans, LA"}]
        artists = util.get_artists(album_artists)
        big_tymers = models.Artist.objects.get(pk=big_tymers.id)

        self.assertEqual(artists, [big_tymers])
        self.assertEqual(big_tymers.hometown, "New Orleans, LA")

    def test_do_not_update_artist_if_hometown_is_not_submitted(self):
        big_tymers = models.Artist.objects.create(
            name="Big Tymers", hometown="New Orleans, LA"
        )
        album_artists = [{"name": "Big Tymers", "hometown": ""}]
        artists = util.get_artists(album_artists)
        big_tymers = models.Artist.objects.get(pk=big_tymers.id)

        self.assertEqual(artists, [big_tymers])
        self.assertEqual(big_tymers.hometown, "New Orleans, LA")


class StripWhitespaceTestCase(TestCase):
    def test_extraneous_whitespace_is_stripped(self):
        album_data = {
            "artist": "  Lil   Wayne ",
            "album": " Tha  Block Is    Hot   ",
            "release_date": "   1999-11-02  ",
        }
        stripped_data = util.strip_whitespace(album_data)

        self.assertEqual(stripped_data["artist"], "Lil Wayne")
        self.assertEqual(stripped_data["album"], "Tha Block Is Hot")
        self.assertEqual(stripped_data["release_date"], "1999-11-02")

    def test_fields_with_no_extraneous_whitespace_are_unaffected(self):
        album_data = {
            "artist": "Juvenile",
            "album": "    400  Degreez    ",
            "release_date": "1998-11-03",
        }
        stripped_data = util.strip_whitespace(album_data)

        self.assertEqual(stripped_data["artist"], "Juvenile")
        self.assertEqual(stripped_data["album"], "400 Degreez")
        self.assertEqual(stripped_data["release_date"], "1998-11-03")

    def test_nonstring_fields_are_unaffected(self):
        album_data = {
            "artist": " Hot  Boys   ",
            "album": "  Guerrilla   Warfare ",
            "release_date": "   1999-07-27  ",
            "track_count": 17,
            "compilation": False,
        }
        stripped_data = util.strip_whitespace(album_data)

        self.assertEqual(stripped_data["artist"], "Hot Boys")
        self.assertEqual(stripped_data["album"], "Guerrilla Warfare")
        self.assertEqual(stripped_data["release_date"], "1999-07-27")
        self.assertEqual(stripped_data["track_count"], 17)
        self.assertFalse(stripped_data["compilation"])
