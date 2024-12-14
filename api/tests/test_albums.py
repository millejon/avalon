from typing import Any

from django.test import TestCase, Client
from django.http import HttpResponse
from django.urls import reverse


class CreateAlbumTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def setUp(self):
        self.metadata = {
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
        }

    def send_post_request(self, data: dict[str, Any]) -> HttpResponse:
        """Send POST request to API endpoint that creates an Album object.

        Arguments:
            data (dict) -- A dictionary that contains the metadata for
            the album to be added to the database.

        Returns:
            HttpResponse object with the results of the POST request.
        """
        return self.client.post(
            reverse("api:create_album"),
            data=data,
            content_type="application/json",
        )

    def test_create_album_status_code(self):
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 201)

    def test_create_album_json_response_title(self):
        response = self.send_post_request(self.metadata).json()

        self.assertEqual(response["title"], self.metadata["title"])

    def test_create_album_json_response_artists(self):
        response = self.send_post_request(self.metadata).json()
        artists = response["artists"]

        self.assertEqual(artists[0]["name"], self.metadata["artists"][0]["name"])
        self.assertTrue(artists[0]["url"].endswith(f"/api/artists/{artists[0]["id"]}"))
        self.assertFalse("hometown" in artists[0].keys())

    def test_create_album_json_response_release_date(self):
        response = self.send_post_request(self.metadata).json()

        self.assertEqual(response["release_date"], self.metadata["release_date"])

    def test_create_album_json_response_label(self):
        response = self.send_post_request(self.metadata).json()

        self.assertEqual(response["label"], self.metadata["label"])

    def test_create_album_json_response_tracklist(self):
        response = self.send_post_request(self.metadata).json()
        tracklist = response["tracklist"]

        self.assertEqual(tracklist["count"], 0)
        self.assertTrue(tracklist["url"].endswith(f"api/albums/{response["id"]}/songs"))

    def test_create_album_json_response_length(self):
        response = self.send_post_request(self.metadata).json()

        self.assertEqual(response["length"], 0)

    def test_create_album_json_response_album_type(self):
        response = self.send_post_request(self.metadata).json()

        self.assertEqual(response["album_type"], self.metadata["album_type"])

    def test_create_album_json_response_url(self):
        response = self.send_post_request(self.metadata).json()

        self.assertTrue(response["url"].endswith(f"api/albums/{response["id"]}"))

    def test_create_album_without_label(self):
        del self.metadata["label"]
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 201)
        self.assertIsNone(response.json()["label"])

    def test_create_album_without_album_type(self):
        del self.metadata["album_type"]
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["album_type"], "album")

    def test_create_album_with_extraneous_whitespace(self):
        self.metadata["title"] = "   Vol. 2,  Hard    Knock Life  "
        self.metadata["artists"][0]["name"] = "  Jay-Z "
        self.metadata["label"] = " Roc-A-Fella   Records   "
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Vol. 2, Hard Knock Life")
        self.assertEqual(response.json()["artists"][0]["name"], "Jay-Z")
        self.assertEqual(response.json()["label"], "Roc-A-Fella Records")

    def test_create_album_with_extraneous_fields(self):
        self.metadata["art_design"] = "The Drawing Board"
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 201)
        self.assertFalse("art_design" in response.json().keys())

    def test_create_duplicate_album(self):
        self.send_post_request(self.metadata)
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["error"], "Album already exists in database.")

    def test_create_album_with_missing_required_fields(self):
        del self.metadata["release_date"]
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 422)

    def test_create_album_with_invalid_values(self):
        self.metadata["release_date"] = 19980929
        response = self.send_post_request(self.metadata)

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
