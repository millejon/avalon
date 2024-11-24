from django.test import TestCase, Client
from django.db import IntegrityError
from django.urls import reverse


class CreateArtistTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_create_valid_artist_status_code(self):
        response = self.client.post(
            reverse("api:create_artist"),
            {"name": "The Notorious B.I.G.", "hometown": "New York, NY"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_artist_json_response(self):
        response = self.client.post(
            reverse("api:create_artist"),
            {"name": "The Notorious B.I.G.", "hometown": "New York, NY"},
            content_type="application/json",
        ).json()

        self.assertEqual(response["name"], "The Notorious B.I.G.")
        self.assertEqual(response["hometown"], "New York, NY")
        self.assertEqual(response["albums"]["count"], 0)
        self.assertTrue(
            response["albums"]["url"].endswith(f"/api/artists/{response["id"]}/albums")
        )
        self.assertEqual(response["singles"]["count"], 0)
        self.assertTrue(
            response["singles"]["url"].endswith(
                f"/api/artists/{response["id"]}/singles"
            )
        )
        self.assertTrue(response["url"].endswith(f"/api/artists/{response["id"]}"))

    def test_create_valid_artist_without_optional_fields_status_code(self):
        response = self.client.post(
            reverse("api:create_artist"),
            {"name": "Mase"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_artist_without_optional_fields_json_response(self):
        response = self.client.post(
            reverse("api:create_artist"),
            {"name": "Mase"},
            content_type="application/json",
        ).json()

        self.assertEqual(response["name"], "Mase")
        self.assertIsNone(response["hometown"])
        self.assertTrue(response["url"].endswith(f"/api/artists/{response["id"]}"))

    def test_create_artist_with_extraneous_whitespace(self):
        response = self.client.post(
            reverse("api:create_artist"),
            {"name": "  Black   Rob ", "hometown": "    New York,  NY  "},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "Black Rob")
        self.assertEqual(response.json()["hometown"], "New York, NY")

    def test_create_artist_with_extraneous_fields(self):
        response = self.client.post(
            reverse("api:create_artist"),
            {"name": "Puff Daddy", "hometown": "New York, NY", "alias": "Diddy"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "Puff Daddy")
        self.assertFalse("alias" in response.json().keys())

    def test_create_duplicate_artist(self):
        self.client.post(
            reverse("api:create_artist"),
            {"name": "Lil Kim", "hometown": "New York, NY"},
            content_type="application/json",
        )

        response = self.client.post(
            reverse("api:create_artist"),
            {"name": "lil kim"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Artist already exists in database.")

    def test_create_artist_with_missing_required_fields(self):
        response = self.client.post(
            reverse("api:create_artist"),
            {"hometown": "Yonkers, NY"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_create_artist_with_invalid_values(self):
        response = self.client.post(
            reverse("api:create_artist"),
            {"name": 112, "hometown": 30349},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)
