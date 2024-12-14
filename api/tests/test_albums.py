from typing import Any

from django.test import TestCase, Client
from django.http import HttpResponse
from django.urls import reverse


class CreateAlbumTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_create_valid_album_status_code(self):
        response = self.client.post(
            reverse("api:create_album"),
            data={
                "title": "Vol. 2, Hard Knock Life",
                "artists": [
                    {
                        "name": "Jay-Z",
                        "hometown": "New York, NY",
                    }
                ],
                "release_date": "1998-09-29",
                "label": "Roc-A-Fella Records",
                "album_type": "album",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_album_json_response(self):
        response = self.client.post(
            reverse("api:create_album"),
            data={
                "title": "Vol. 2, Hard Knock Life",
                "artists": [
                    {
                        "name": "Jay-Z",
                        "hometown": "New York, NY",
                    }
                ],
                "release_date": "1998-09-29",
                "label": "Roc-A-Fella Records",
                "album_type": "album",
            },
            content_type="application/json",
        ).json()

        self.assertEqual(response["title"], "Vol. 2, Hard Knock Life")
        self.assertEqual(response["artists"][0]["name"], "Jay-Z")
        self.assertTrue(
            response["artists"][0]["url"].endswith(
                f"/api/artists/{response["artists"][0]["id"]}"
            )
        )
        self.assertEqual(response["release_date"], "1998-09-29")
        self.assertEqual(response["label"], "Roc-A-Fella Records")
        self.assertEqual(response["album_type"], "album")
        self.assertTrue(response["url"].endswith(f"api/albums/{response["id"]}"))

    def test_create_valid_album_without_optional_fields_status_code(self):
        response = self.client.post(
            reverse("api:create_album"),
            data={
                "title": "Coming Of Age",
                "artists": [
                    {
                        "name": "Memphis Bleek",
                        "hometown": "New York, NY",
                    }
                ],
                "release_date": "1999-08-03",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_album_without_optional_fields_json_response(self):
        response = self.client.post(
            reverse("api:create_album"),
            data={
                "title": "Coming Of Age",
                "artists": [
                    {
                        "name": "Memphis Bleek",
                        "hometown": "New York, NY",
                    }
                ],
                "release_date": "1999-08-03",
            },
            content_type="application/json",
        ).json()

        self.assertEqual(response["title"], "Coming Of Age")
        self.assertEqual(response["artists"][0]["name"], "Memphis Bleek")
        self.assertTrue(
            response["artists"][0]["url"].endswith(
                f"/api/artists/{response["artists"][0]["id"]}"
            )
        )
        self.assertEqual(response["release_date"], "1999-08-03")
        self.assertIsNone(response["label"])
        self.assertEqual(response["album_type"], "album")
        self.assertTrue(response["url"].endswith(f"api/albums/{response["id"]}"))

    def test_create_album_with_extraneous_whitespace(self):
        response = self.client.post(
            reverse("api:create_album"),
            data={
                "title": "  The    Professional ",
                "artists": [
                    {
                        "name": " DJ   Clue  ",
                        "hometown": "New York, NY",
                    }
                ],
                "release_date": "1998-12-15",
                "label": "   Roc-A-Fella  Records   ",
                "album_type": "album",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "The Professional")
        self.assertEqual(response.json()["artists"][0]["name"], "DJ Clue")
        self.assertEqual(response.json()["label"], "Roc-A-Fella Records")

    def test_create_album_with_extraneous_fields(self):
        response = self.client.post(
            reverse("api:create_album"),
            data={
                "title": "The Truth",
                "artists": [
                    {
                        "name": "Beanie Sigel",
                        "hometown": "Philadelphia, PA",
                    }
                ],
                "release_date": "2000-02-29",
                "label": "Roc-A-Fella Records",
                "album_type": "album",
                "executive_producers": ["Jay-Z", "Damon Dash", "Kareem Burke"],
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "The Truth")
        self.assertFalse("executive_producers" in response.json().keys())

    def test_create_duplicate_album(self):
        self.client.post(
            reverse("api:create_album"),
            data={
                "title": "Reasonable Doubt",
                "artists": [{"name": "Jay-Z", "hometown": "New York, NY"}],
                "release_date": "1996-06-25",
                "label": "Roc-A-Fella Records",
                "album_type": "album",
            },
            content_type="application/json",
        )

        response = self.client.post(
            reverse("api:create_album"),
            data={
                "title": "reasonable doubt",
                "artists": [{"name": "Jay-Z"}],
                "release_date": "1996-06-25",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Album already exists in database.")

    def test_create_album_with_missing_required_fields(self):
        response = self.client.post(
            reverse("api:create_album"),
            {"title": "All Money Is Legal"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_create_album_with_invalid_values(self):
        response = self.client.post(
            reverse("api:create_album"),
            data={
                "title": 534,
                "artists": [{"name": "Memphis Bleek", "hometown": "New York, NY"}],
                "release_date": "2005-05-17",
                "label": "Roc-A-Fella Records",
                "album_type": "album",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)


class CreateSongTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.come_home_with_me = cls.client.post(
            reverse("api:create_album"),
            data={
                "title": "Come Home With Me",
                "artists": [{"name": "Cam'ron", "hometown": "New York, NY"}],
                "release_date": "2002-05-14",
                "label": "Roc-A-Fella Records",
                "album_type": "album",
            },
            content_type="application/json",
        ).json()

    def setUp(self):
        self.metadata = {
            "title": "Welcome To New York City",
            "artists": [
                {"name": "Cam'ron"},
                {"name": "Jay-Z"},
                {"name": "Juelz Santana"},
            ],
            "group_members": [{"name": "The Diplomats"}],
            "producers": [{"name": "Just Blaze"}],
            "disc": 1,
            "track_number": 7,
            "length": 309,
            "path": "/camron/come-home-with-me/07_welcome_to_new_york_city.flac",
        }

    def send_post_request(self, data: dict[str, Any]) -> HttpResponse:
        """Send POST request to API endpoint that creates a Song object.

        Arguments:
            data (dict) -- A dictionary that contains the metadata for
            the song to be added to the database.

        Returns:
            HttpResponse object with the results of the POST request.
        """
        return self.client.post(
            reverse("api:create_song", kwargs={"id": self.come_home_with_me["id"]}),
            data=data,
            content_type="application/json",
        )

    def test_create_song_status_code(self):
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 201)

    def test_create_song_json_response_title(self):
        response = self.send_post_request(self.metadata).json()

        self.assertEqual(response["title"], self.metadata["title"])

    def test_create_song_json_response_artists(self):
        response = self.send_post_request(self.metadata).json()
        artists = response["artists"]

        self.assertEqual(artists[0]["name"], self.metadata["artists"][0]["name"])
        self.assertTrue(artists[0]["url"].endswith(f"/api/artists/{artists[0]["id"]}"))
        self.assertEqual(artists[1]["name"], self.metadata["artists"][1]["name"])
        self.assertTrue(artists[1]["url"].endswith(f"/api/artists/{artists[1]["id"]}"))
        self.assertEqual(artists[2]["name"], self.metadata["artists"][2]["name"])
        self.assertTrue(artists[2]["url"].endswith(f"/api/artists/{artists[2]["id"]}"))

    def test_create_song_json_response_group_members(self):
        response = self.send_post_request(self.metadata).json()
        group_members = response["group_members"]

        self.assertEqual(
            group_members[0]["name"], self.metadata["group_members"][0]["name"]
        )
        self.assertTrue(
            group_members[0]["url"].endswith(f"/api/artists/{group_members[0]["id"]}")
        )

    def test_create_song_json_response_producers(self):
        response = self.send_post_request(self.metadata).json()
        producers = response["producers"]

        self.assertEqual(producers[0]["name"], self.metadata["producers"][0]["name"])
        self.assertTrue(
            producers[0]["url"].endswith(f"/api/artists/{producers[0]["id"]}")
        )

    def test_create_song_json_response_album_title(self):
        response = self.send_post_request(self.metadata).json()
        album = response["album"]

        self.assertEqual(album["title"], self.come_home_with_me["title"])

    def test_create_song_json_response_album_artists(self):
        response = self.send_post_request(self.metadata).json()
        album_artists = response["album"]["artists"]

        self.assertEqual(
            album_artists[0]["name"], self.come_home_with_me["artists"][0]["name"]
        )
        self.assertTrue(
            album_artists[0]["url"].endswith(
                f"/api/artists/{self.come_home_with_me["artists"][0]["id"]}"
            )
        )

    def test_create_song_json_response_album_release_date(self):
        response = self.send_post_request(self.metadata).json()
        album = response["album"]

        self.assertEqual(album["release_date"], self.come_home_with_me["release_date"])

    def test_create_song_json_response_album_url(self):
        response = self.send_post_request(self.metadata).json()
        album = response["album"]

        self.assertTrue(
            album["url"].endswith(f"/api/albums/{self.come_home_with_me["id"]}")
        )

    def test_create_song_json_response_disc(self):
        response = self.send_post_request(self.metadata).json()

        self.assertEqual(response["disc"], self.metadata["disc"])

    def test_create_song_json_response_track_number(self):
        response = self.send_post_request(self.metadata).json()

        self.assertEqual(response["track_number"], self.metadata["track_number"])

    def test_create_song_json_response_length(self):
        response = self.send_post_request(self.metadata).json()

        self.assertEqual(response["length"], self.metadata["length"])

    def test_create_song_json_response_path(self):
        response = self.send_post_request(self.metadata).json()

        self.assertEqual(response["path"], self.metadata["path"])

    def test_create_song_json_response_play_count(self):
        response = self.send_post_request(self.metadata).json()

        self.assertEqual(response["play_count"], 0)

    def test_create_song_json_response_url(self):
        response = self.send_post_request(self.metadata).json()

        self.assertTrue(response["url"].endswith(f"/api/songs/{response["id"]}"))

    def test_create_song_without_group_members(self):
        del self.metadata["group_members"]
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 201)
        self.assertIsNone(response.json()["group_members"])

    def test_create_song_without_producers(self):
        del self.metadata["producers"]
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 201)
        self.assertIsNone(response.json()["producers"])

    def test_create_song_without_disc(self):
        del self.metadata["disc"]
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["disc"], 1)

    def test_create_song_with_extraneous_whitespace(self):
        self.metadata["title"] = "   Welcome  To New   York    City "
        self.metadata["artists"][2]["name"] = " Juelz Santana  "
        self.metadata["group_members"][0]["name"] = "  The    Diplomats   "
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Welcome To New York City")
        self.assertEqual(response.json()["artists"][2]["name"], "Juelz Santana")
        self.assertEqual(response.json()["group_members"][0]["name"], "The Diplomats")

    def test_create_song_with_extraneous_fields(self):
        self.metadata["engineer"] = "Young Guru"
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 201)
        self.assertFalse("engineer" in response.json().keys())

    def test_create_song_with_album_that_does_not_exist(self):
        album_id = int(self.come_home_with_me["id"]) + 100
        response = self.client.post(
            reverse("api:create_song", kwargs={"id": album_id}),
            data=self.metadata,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Album with id = {album_id} does not exist."
        )

    def test_create_duplicate_song(self):
        self.send_post_request(self.metadata)
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["error"], "Song already exists in database.")

    def test_create_song_with_duplicate_track_number(self):
        self.send_post_request(self.metadata)
        self.metadata["path"] = "/camron/come-home-with-me/07_welcome_to_nyc.flac"
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.json()["error"],
            f"Album already has a song with track number = {self.metadata["track_number"]}.",
        )

    def test_create_song_with_invalid_disc(self):
        self.metadata["disc"] = 0
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"], "Disc must be a positive integer greater than 0."
        )

    def test_create_song_with_invalid_track_number(self):
        self.metadata["track_number"] = 0
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"],
            "Track number must be a positive integer greater than 0.",
        )

    def test_create_song_with_missing_required_fields(self):
        del self.metadata["length"]
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 422)

    def test_create_song_with_invalid_values(self):
        self.metadata["track_number"] = "Seven"
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 422)
