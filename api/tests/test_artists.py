from typing import Any

from django.test import TestCase, Client
from django.http import HttpResponse
from django.urls import reverse


class CreateArtistTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def setUp(self):
        self.metadata = {"name": "The Notorious B.I.G.", "hometown": "New York, NY"}

    def send_post_request(self, data: dict[str, Any]) -> HttpResponse:
        """Send POST request to API endpoint that creates an Artist object.

        Arguments:
            data (dict) -- A dictionary that contains the metadata for
            the artist to be added to the database.

        Returns:
            HttpResponse object with the results of the POST request.
        """
        return self.client.post(
            reverse("api:create_artist"),
            data=data,
            content_type="application/json",
        )

    def test_create_artist_status_code(self):
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 201)

    def test_create_artist_json_response_name(self):
        response = self.send_post_request(self.metadata).json()

        self.assertEqual(response["name"], self.metadata["name"])

    def test_create_artist_json_response_hometown(self):
        response = self.send_post_request(self.metadata).json()

        self.assertEqual(response["hometown"], self.metadata["hometown"])

    def test_create_artist_json_response_albums(self):
        response = self.send_post_request(self.metadata).json()
        albums = response["albums"]

        self.assertEqual(albums["count"], 0)
        self.assertTrue(albums["url"].endswith(f"/api/artists/{response["id"]}/albums"))

    def test_create_artist_json_response_singles(self):
        response = self.send_post_request(self.metadata).json()
        singles = response["singles"]

        self.assertEqual(singles["count"], 0)
        self.assertTrue(
            singles["url"].endswith(f"/api/artists/{response["id"]}/singles")
        )

    def test_create_artist_json_response_songs(self):
        response = self.send_post_request(self.metadata).json()
        songs = response["songs"]

        self.assertEqual(songs["count"], 0)
        self.assertTrue(songs["url"].endswith(f"/api/artists/{response["id"]}/songs"))

    def test_create_artist_json_response_songs_produced(self):
        response = self.send_post_request(self.metadata).json()
        songs_produced = response["songs_produced"]

        self.assertEqual(songs_produced["count"], 0)
        self.assertTrue(
            songs_produced["url"].endswith(
                f"/api/artists/{response["id"]}/songs-produced"
            )
        )

    def test_create_artist_json_response_url(self):
        response = self.send_post_request(self.metadata).json()

        self.assertTrue(response["url"].endswith(f"/api/artists/{response["id"]}"))

    def test_create_artist_without_hometown(self):
        del self.metadata["hometown"]
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 201)
        self.assertIsNone(response.json()["hometown"])

    def test_create_artist_with_extraneous_whitespace(self):
        self.metadata["name"] = "   The  Notorious B.I.G. "
        self.metadata["hometown"] = " New   York, NY  "
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "The Notorious B.I.G.")
        self.assertEqual(response.json()["hometown"], "New York, NY")

    def test_create_artist_with_extraneous_fields(self):
        self.metadata["alias"] = "Biggie"
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 201)
        self.assertFalse("alias" in response.json().keys())

    def test_create_duplicate_artist(self):
        self.send_post_request(self.metadata)
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["error"], "Artist already exists in database.")

    def test_create_artist_with_missing_required_fields(self):
        del self.metadata["name"]
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 422)

    def test_create_artist_with_invalid_values(self):
        self.metadata["hometown"] = 11216
        response = self.send_post_request(self.metadata)

        self.assertEqual(response.status_code, 422)
