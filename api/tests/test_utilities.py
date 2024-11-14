from django.test import TestCase

from api import utilities as util


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
