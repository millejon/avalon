from django.test import TestCase

from api import utilities as util


class StripWhitespaceTestCase(TestCase):

    def test_extraneous_whitespace_is_stripped(self):
        data = {
            "name": " Boldy   James ",
            "album": "Mr. Ten08   ",
            "producer": "   Futurewave",
        }
        stripped_data = util.strip_whitespace(data)

        self.assertEqual(stripped_data["name"], "Boldy James")
        self.assertEqual(stripped_data["album"], "Mr. Ten08")
        self.assertEqual(stripped_data["producer"], "Futurewave")

    def test_fields_with_no_extraneous_whitespace_are_unaffected(self):
        data = {
            "name": "Rome Streetz",
            "album": "Death & The Magician",
            "producer": "DJ Muggs",
        }
        stripped_data = util.strip_whitespace(data)

        self.assertEqual(stripped_data["name"], "Rome Streetz")
        self.assertEqual(stripped_data["album"], "Death & The Magician")
        self.assertEqual(stripped_data["producer"], "DJ Muggs")

    def test_nonstring_fields_are_unaffected(self):
        data = {
            "name": "Conway  The      Machine    ",
            "album": "    Speshal Machinery:      The Ghronic Edition  ",
            "producer": "  Big Ghost Ltd.",
            "track_count": 9,
            "single": False,
        }
        stripped_data = util.strip_whitespace(data)

        self.assertEqual(stripped_data["name"], "Conway The Machine")
        self.assertEqual(
            stripped_data["album"], "Speshal Machinery: The Ghronic Edition"
        )
        self.assertEqual(stripped_data["producer"], "Big Ghost Ltd.")
        self.assertEqual(stripped_data["track_count"], 9)
        self.assertFalse(stripped_data["single"])


class NormalizeTextTestCase(TestCase):
    def test_remove_punctuation_from_string(self):
        text = util.normalize_text("!\"$G%'(r)*,I-.s/:;E<>?@[l\\]^D_`{A|}~")

        self.assertEqual(text, "griselda")

    def test_replace_punctuation_in_string(self):
        text = util.normalize_text("Hall & Nash + Alchemist = # 2")

        self.assertEqual(text, "hall and nash and alchemist equal number 2")

    def test_remove_capitalization_with_no_punctuation(self):
        text = util.normalize_text("Pray For PARIS")

        self.assertEqual(text, "pray for paris")
