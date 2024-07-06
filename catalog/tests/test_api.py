from django.test import TestCase, Client
from django.db import IntegrityError
from django.urls import reverse


class CreateArtistTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_create_artist(self):
        response = self.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Future"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

        response = response.json()
        artist_id = response["id"]

        self.assertEqual(response["name"], "Future")
        self.assertTrue(response["url"].endswith(f"/api/v1/artists/{artist_id}"))
        self.assertEqual(response["albums"]["count"], 0)
        self.assertTrue(
            response["albums"]["url"].endswith(f"/api/v1/artists/{artist_id}/albums/")
        )
        self.assertEqual(response["singles"]["count"], 0)
        self.assertTrue(
            response["singles"]["url"].endswith(f"/api/v1/artists/{artist_id}/singles/")
        )
        self.assertEqual(response["songs"]["count"], 0)
        self.assertTrue(
            response["songs"]["url"].endswith(f"/api/v1/artists/{artist_id}/songs/")
        )
        self.assertEqual(response["songs_produced"]["count"], 0)
        self.assertTrue(
            response["songs_produced"]["url"].endswith(
                f"/api/v1/artists/{artist_id}/produced/"
            )
        )

    def test_create_artist_with_whitespace(self):
        response = self.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "   French Montana   "},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "French Montana")

    def test_create_duplicate_artist(self):
        self.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Don Toliver"},
            content_type="application/json",
        )

        with self.assertRaises(IntegrityError):
            self.client.post(
                reverse("api-1.0:create_artist"),
                {"name": "Don Toliver"},
                content_type="application/json",
            )

    def test_create_artist_with_missing_required_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_artist"),
            {"label": "Def Jam Recordings"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_create_artist_with_invalid_values(self):
        response = self.client.post(
            reverse("api-1.0:create_artist"),
            {"name": 42},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)
