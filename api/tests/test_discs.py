from django.test import TestCase, Client
from django.db import IntegrityError
from django.urls import reverse


class CreateDisc(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.notorious_big = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "The Notorious B.I.G."},
            content_type="application/json",
        ).json()
        cls.life_after_death = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "artists": [cls.notorious_big["id"]],
                "title": "Life After Death",
                "release_date": "1997-03-25",
                "multidisc": True,
            },
            content_type="application/json",
        ).json()

    def test_create_valid_disc_status_code(self):
        response = self.client.post(
            reverse("api-1.0:create_disc"),
            {
                "album": self.life_after_death["id"],
                "title": "Disc One",
                "number": 1,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_disc_json_response(self):
        response = self.client.post(
            reverse("api-1.0:create_disc"),
            {
                "album": self.life_after_death["id"],
                "title": "Disc One",
                "number": 1,
            },
            content_type="application/json",
        ).json()

        self.assertEqual(response["album"]["title"], "Life After Death")
        self.assertEqual(response["title"], "Disc One")
        self.assertEqual(response["number"], 1)
        self.assertTrue(response["url"].endswith(f"/api/v1/discs/{response["id"]}"))
        self.assertIsNone(response["tracklist"])

    def test_create_disc_with_extraneous_whitespace(self):
        response = self.client.post(
            reverse("api-1.0:create_disc"),
            {
                "album": self.life_after_death["id"],
                "title": "Disc Two    ",
                "number": 2,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Disc Two")

    def test_create_disc_with_extraneous_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_disc"),
            {
                "album": self.life_after_death["id"],
                "title": "Disc One",
                "number": 1,
                "track_count": 12,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Disc One")
        self.assertFalse("track_count" in response.json().keys())

    def test_create_duplicate_disc(self):
        self.client.post(
            reverse("api-1.0:create_disc"),
            {
                "album": self.life_after_death["id"],
                "title": "Disc One",
                "number": 1,
            },
            content_type="application/json",
        )

        with self.assertRaises(IntegrityError):
            self.client.post(
                reverse("api-1.0:create_disc"),
                {
                    "album": self.life_after_death["id"],
                    "title": "Disc One",
                    "number": 1,
                },
                content_type="application/json",
            )

    def test_create_disc_with_missing_required_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_disc"),
            {
                "album": self.life_after_death["id"],
                "title": "Disc One",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_create_disc_with_invalid_values(self):
        response = self.client.post(
            reverse("api-1.0:create_disc"),
            {
                "album": "Life After Death",
                "title": "Disc One",
                "number": 1,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)
