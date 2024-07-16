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
                "title": "Skew It On The Bar-B",
                "track_number": 4,
                "length": 195,
                "path": "/archive/outkast/aquemini/04_skew_it_on_the_barb.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_song_json_response(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "album": self.aquemini["id"],
                "title": "Skew It On The Bar-B",
                "track_number": 4,
                "length": 195,
                "path": "/archive/outkast/aquemini/04_skew_it_on_the_barb.flac",
            },
            content_type="application/json",
        ).json()

        self.assertEqual(len(response["artists"]), 0)
        self.assertEqual(response["album"]["title"], "Aquemini")
        self.assertIsNone(response["disc"])
        self.assertEqual(response["track_number"], 4)
        self.assertEqual(response["title"], "Skew It On The Bar-B")
        self.assertEqual(response["length"], 195)
        self.assertEqual(response["play_count"], 0)
        self.assertEqual(response["path"], "/archive/outkast/aquemini/04_skew_it_on_the_barb.flac")
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
                "title": "       Skew It On The Bar-B     ",
                "track_number": 4,
                "length": 195,
                "path": "/archive/outkast/aquemini/04_skew_it_on_the_barb.flac       ",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Skew It On The Bar-B")
        self.assertEqual(response.json()["path"], "/archive/outkast/aquemini/04_skew_it_on_the_barb.flac")

    def test_create_song_with_extraneous_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "album": self.aquemini["id"],
                "title": "Skew It On The Bar-B",
                "track_number": 4,
                "length": 195,
                "path": "/archive/outkast/aquemini/04_skew_it_on_the_barb.flac",
                "writers": ["Morton Stevens", "Organized Noize", "Antwan Patton", "André Benjamin", "Corey Woods"],
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Skew It On The Bar-B")
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
                "title": "Skew It On The Bar-B",
                "track_number": 4,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_create_song_with_invalid_values(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "album": "Aquemini",
                "title": "Skew It On The Bar-B",
                "track_number": 4,
                "length": 195,
                "path": "/archive/outkast/aquemini/04_skew_it_on_the_barb.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)


class RetrieveSong(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.ugk = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "UGK"},
            content_type="application/json",
        ).json()
        cls.aquemini = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "artists": [cls.ugk["id"]],
                "title": "Ridin' Dirty",
                "release_date": "1996-07-30",
            },
            content_type="application/json",
        ).json()
        cls.hilife = cls.client.post(
            reverse("api-1.0:create_song"),
            {
                "album": cls.aquemini["id"],
                "title": "Hi-Life",
                "track_number": 10,
                "length": 325,
                "path": "/archive/ugk/ridin-dirty/10_hilife.flac",
            },
            content_type="application/json",
        ).json()

    def test_retrieve_song_status_code(self):
        response = self.client.get(
            reverse("api-1.0:retrieve_song", kwargs={"id": self.hilife["id"]})
        )

        self.assertEqual(response.status_code, 200)

    def test_retrieve_song_json_response(self):
        response = self.client.get(
            reverse("api-1.0:retrieve_song", kwargs={"id": self.hilife["id"]})
        ).json()

        self.assertEqual(len(response["artists"]), 0)
        self.assertEqual(response["album"]["title"], "Ridin' Dirty")
        self.assertIsNone(response["disc"])
        self.assertEqual(response["track_number"], 10)
        self.assertEqual(response["title"], "Hi-Life")
        self.assertEqual(response["length"], 325)
        self.assertEqual(response["play_count"], 0)
        self.assertEqual(response["path"], "/archive/ugk/ridin-dirty/10_hilife.flac")
        self.assertTrue(response["url"].endswith(f"/api/v1/songs/{response["id"]}"))

    def test_retrieve_unknown_song(self):
        song_id = self.hilife["id"] + 1
        response = self.client.get(
            reverse("api-1.0:retrieve_song", kwargs={"id": song_id})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Song with id = {song_id} does not exist."
        )


class UpdateSong(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.scarface = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Scarface"},
            content_type="application/json",
        ).json()
        cls.my_homies = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "artists": [cls.scarface["id"]],
                "title": "My Homies",
                "release_date": "1998-03-03",
                "multidisc": True,
            },
            content_type="application/json",
        ).json()
        cls.disc1 = cls.client.post(
            reverse("api-1.0:create_disc"),
            {
                "album": cls.my_homies["id"],
                "title": "Disc 1",
                "number": 1,
            },
            content_type="application/json",
        ).json()
        cls.win_lose_or_draw = cls.client.post(
            reverse("api-1.0:create_song"),
            {
                "album": cls.my_homies["id"],
                "title": "Win, Lose, or Draw",
                "track_number": 12,
                "length": 316,
                "path": "/archive/scarface/my-homies/disc-1/12_win_lose_or_draw.flac",
            },
            content_type="application/json",
        ).json()

    def test_update_song_status_code(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.win_lose_or_draw["id"]}),
            {
                "album": self.my_homies["id"],
                "title": "Win Lose or Draw",
                "track_number": 12,
                "length": 316,
                "path": "/archive/scarface/my-homies/disc-1/12_win_lose_or_draw.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

    def test_update_song_json_response(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.win_lose_or_draw["id"]}),
            {
                "album": self.my_homies["id"],
                "disc": self.disc1["id"],
                "title": "Win Lose or Draw",
                "track_number": 12,
                "length": 316,
                "path": "/archive/scarface/my-homies/disc-1/12_win_lose_or_draw.flac",
            },
            content_type="application/json",
        ).json()

        self.assertEqual(len(response["artists"]), 0)
        self.assertEqual(response["album"]["title"], "My Homies")
        self.assertEqual(response["disc"], 1)
        self.assertEqual(response["track_number"], 12)
        self.assertEqual(response["title"], "Win Lose or Draw")
        self.assertEqual(response["length"], 316)
        self.assertEqual(response["play_count"], 0)
        self.assertEqual(response["path"], "/archive/scarface/my-homies/disc-1/12_win_lose_or_draw.flac")
        self.assertTrue(response["url"].endswith(f"/api/v1/songs/{response["id"]}"))

    def test_update_song_with_extraneous_whitespace(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.win_lose_or_draw["id"]}),
            {
                "album": self.my_homies["id"],
                "disc": self.disc1["id"],
                "title": "Win Lose or Draw      ",
                "track_number": 12,
                "length": 316,
                "path": "     /archive/scarface/my-homies/disc-1/12_win_lose_or_draw.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Win Lose or Draw")
        self.assertEqual(response.json()["path"], "/archive/scarface/my-homies/disc-1/12_win_lose_or_draw.flac")

    def test_update_song_with_extraneous_fields(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.win_lose_or_draw["id"]}),
            {
                "album": self.my_homies["id"],
                "disc": self.disc1["id"],
                "title": "Win Lose or Draw",
                "track_number": 12,
                "length": 316,
                "publisher": "N The Water Publishing, Inc.",
                "path": "/archive/scarface/my-homies/disc-1/12_win_lose_or_draw.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Win Lose or Draw")
        self.assertFalse("publisher" in response.json().keys())

    def test_update_song_with_missing_required_fields(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.win_lose_or_draw["id"]}),
            {
                "album": self.my_homies["id"],
                "disc": self.disc1["id"],
                "title": "Win Lose or Draw",
                "length": 316,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_update_song_with_invalid_values(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.win_lose_or_draw["id"]}),
            {
                "album": "My Homies",
                "disc": "Disc 1",
                "title": "Win Lose or Draw",
                "track_number": 12,
                "length": 316,
                "path": "/archive/scarface/my-homies/disc-1/12_win_lose_or_draw.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_update_unknown_song(self):
        song_id = self.win_lose_or_draw["id"] + 1
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": song_id}),
            {
                "album": self.my_homies["id"],
                "disc": self.disc1["id"],
                "title": "Overnight",
                "track_number": 13,
                "length": 249,
                "path": "/archive/scarface/my-homies/disc-1/13_overnight.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Song with id = {song_id} does not exist."
        )
