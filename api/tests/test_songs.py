from django.test import TestCase, Client
from django.db import IntegrityError
from django.urls import reverse


class CreateSong(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.outkast = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Outkast"},
            content_type="application/json",
        ).json()
        cls.aquemini = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "artists": [cls.outkast["id"]],
                "title": "Aquemini",
                "release_date": "1998-09-29",
            },
            content_type="application/json",
        ).json()
        cls.speakerboxxx = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "artists": [cls.outkast["id"]],
                "title": "Speakerboxxx / The Love Below",
                "release_date": "2003-09-23",
                "multidisc": True,
            },
            content_type="application/json",
        ).json()
        cls.the_love_below = cls.client.post(
            reverse("api-1.0:create_disc"),
            {
                "album": cls.speakerboxxx["id"],
                "title": "The Love Below",
                "number": 2,
            },
            content_type="application/json",
        ).json()

    def test_create_valid_song_status_code(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "album": self.aquemini["id"],
                "title": "Return Of The G",
                "track_number": 2,
                "length": 289,
                "path": "/archive/outkast/aquemini/02_return_of_the_g.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_song_json_response(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "album": self.aquemini["id"],
                "title": "Return Of The G",
                "track_number": 2,
                "length": 289,
                "path": "/archive/outkast/aquemini/02_return_of_the_g.flac",
            },
            content_type="application/json",
        ).json()

        self.assertEqual(len(response["artists"]), 0)
        self.assertEqual(response["album"]["title"], "Aquemini")
        self.assertIsNone(response["disc"])
        self.assertEqual(response["track_number"], 2)
        self.assertEqual(response["title"], "Return Of The G")
        self.assertEqual(response["length"], 289)
        self.assertEqual(response["play_count"], 0)
        self.assertEqual(response["path"], "/archive/outkast/aquemini/02_return_of_the_g.flac")
        self.assertTrue(response["url"].endswith(f"/api/v1/songs/{response["id"]}"))

    def test_create_valid_multidisc_song_status_code(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "album": self.speakerboxxx["id"],
                "disc": self.the_love_below["id"],
                "title": "Prototype",
                "track_number": 7,
                "length": 326,
                "path": "/archive/outkast/speakerboxx-the-love-below/the-love-below/07_prototype.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_multidisc_song_json_response(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "album": self.speakerboxxx["id"],
                "disc": self.the_love_below["id"],
                "title": "Prototype",
                "track_number": 7,
                "length": 326,
                "path": "/archive/outkast/speakerboxx-the-love-below/the-love-below/07_prototype.flac",
            },
            content_type="application/json",
        ).json()

        self.assertEqual(len(response["artists"]), 0)
        self.assertEqual(response["album"]["title"], "Speakerboxxx / The Love Below")
        self.assertEqual(response["disc"], 2)
        self.assertEqual(response["track_number"], 7)
        self.assertEqual(response["title"], "Prototype")
        self.assertEqual(response["length"], 326)
        self.assertEqual(response["play_count"], 0)
        self.assertEqual(response["path"], "/archive/outkast/speakerboxx-the-love-below/the-love-below/07_prototype.flac")
        self.assertTrue(response["url"].endswith(f"/api/v1/songs/{response["id"]}"))

    def test_create_song_with_extraneous_whitespace(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "album": self.aquemini["id"],
                "title": "       Return Of The G      ",
                "track_number": 2,
                "length": 289,
                "path": "/archive/outkast/aquemini/02_return_of_the_g.flac     ",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Return Of The G")
        self.assertEqual(response.json()["path"], "/archive/outkast/aquemini/02_return_of_the_g.flac")

    def test_create_song_with_extraneous_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "album": self.aquemini["id"],
                "title": "Rosa Parks",
                "track_number": 3,
                "length": 324,
                "path": "/archive/outkast/aquemini/03_rosa_parks.flac",
                "writers": ["André Benjamin", "Antwan Patton"]
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Rosa Parks")
        self.assertFalse("writers" in response.json().keys())

    def test_create_duplicate_song(self):
        self.client.post(
            reverse("api-1.0:create_song"),
            {
                "album": self.aquemini["id"],
                "title": "Skew It On The Bar-B",
                "track_number": 4,
                "length": 195,
                "path": "/archive/outkast/aquemini/04_skew_it_on_the_barb.flac",
            },
            content_type="application/json",
        )

        with self.assertRaises(IntegrityError):
            self.client.post(
                reverse("api-1.0:create_song"),
                {
                    "album": self.aquemini["id"],
                    "title": "Skew It On The Bar-B",
                    "track_number": 4,
                    "length": 195,
                    "path": "/archive/outkast/aquemini/04_skew_it_on_the_barb.flac",
                },
                content_type="application/json",
            )

    def test_create_song_with_missing_required_fields(self):
        response = self.client.post(
                reverse("api-1.0:create_song"),
                {
                    "album": self.aquemini["id"],
                    "title": "Synthesizer",
                    "track_number": 6,
                },
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 422)

    def test_create_song_with_invalid_values(self):
        response = self.client.post(
                reverse("api-1.0:create_song"),
                {
                    "album": "Aquemini",
                    "title": "Slump",
                    "track_number": 7,
                    "length": 309,
                    "path": "/archive/outkast/aquemini/07_slump.flac",
                },
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 422)
