from django.test import TestCase, Client
from django.db import IntegrityError
from django.urls import reverse


class CreateArtist(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_create_valid_artist_status_code(self):
        response = self.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Future"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_artist_json_response(self):
        response = self.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Future"},
            content_type="application/json",
        ).json()
        artist_id = response["id"]

        self.assertEqual(response["name"], "Future")
        self.assertTrue(response["url"].endswith(f"/api/v1/artists/{artist_id}"))
        self.assertIsNone(response["albums"])
        self.assertIsNone(response["singles"])
        self.assertIsNone(response["songs"])
        self.assertIsNone(response["songs_produced"])

    def test_create_artist_with_extraneous_whitespace(self):
        response = self.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "   Future   "},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "Future")

    def test_create_artist_with_extraneous_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Future", "alias": "Future Hendrix"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "Future")
        self.assertFalse("alias" in response.json().keys())

    def test_create_duplicate_artist(self):
        self.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Future"},
            content_type="application/json",
        )

        with self.assertRaises(IntegrityError):
            self.client.post(
                reverse("api-1.0:create_artist"),
                {"name": "Future"},
                content_type="application/json",
            )

    def test_create_artist_with_missing_required_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_artist"),
            {"label": "Freebandz"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_create_artist_with_invalid_values(self):
        response = self.client.post(
            reverse("api-1.0:create_artist"),
            {"name": 2003},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)


class RetrieveArtist(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.tinashe = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Tinashe"},
            content_type="application/json",
        ).json()

    def test_retrieve_artist_status_code(self):
        response = self.client.get(
            reverse("api-1.0:retrieve_artist", kwargs={"id": self.tinashe["id"]})
        )

        self.assertEqual(response.status_code, 200)

    def test_retrieve_artist_json_response(self):
        response = self.client.get(
            reverse("api-1.0:retrieve_artist", kwargs={"id": self.tinashe["id"]})
        ).json()

        self.assertEqual(response["name"], "Tinashe")
        self.assertTrue(response["url"].endswith(f"/api/v1/artists/{self.tinashe["id"]}"))
        self.assertIsNone(response["albums"])
        self.assertIsNone(response["singles"])
        self.assertIsNone(response["songs"])
        self.assertIsNone(response["songs_produced"])

    def test_retrieve_unknown_artist(self):
        artist_id = self.tinashe["id"] + 1
        response = self.client.get(
            reverse("api-1.0:retrieve_artist", kwargs={"id": artist_id})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Artist with id = {artist_id} does not exist."
        )


class UpdateArtist(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.don_toliver = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Don Toliver"},
            content_type="application/json",
        ).json()

    def test_update_artist_status_code(self):
        response = self.client.put(
            reverse("api-1.0:update_artist", kwargs={"id": self.don_toliver["id"]}),
            {"name": "Donny Womack"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

    def test_update_artist_json_response(self):
        response = self.client.put(
            reverse("api-1.0:update_artist", kwargs={"id": self.don_toliver["id"]}),
            {"name": "Donny Womack"},
            content_type="application/json",
        ).json()

        self.assertEqual(response["name"], "Donny Womack")
        self.assertTrue(response["url"].endswith(f"/api/v1/artists/{self.don_toliver["id"]}"))
        self.assertIsNone(response["albums"])
        self.assertIsNone(response["singles"])
        self.assertIsNone(response["songs"])
        self.assertIsNone(response["songs_produced"])

    def test_update_artist_with_extraneous_whitespace(self):
        response = self.client.put(
            reverse("api-1.0:update_artist", kwargs={"id": self.don_toliver["id"]}),
            {"name": "   Donny Womack   "},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Donny Womack")

    def test_update_artist_with_extraneous_fields(self):
        response = self.client.put(
            reverse("api-1.0:update_artist", kwargs={"id": self.don_toliver["id"]}),
            {"name": "Donny Womack", "alias": "Don Toliver"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Donny Womack")
        self.assertFalse("alias" in response.json().keys())

    def test_update_artist_with_missing_required_fields(self):
        response = self.client.put(
            reverse("api-1.0:update_artist", kwargs={"id": self.don_toliver["id"]}),
            {"label": "Cactus Jack Records"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_update_artist_with_invalid_values(self):
        response = self.client.put(
            reverse("api-1.0:update_artist", kwargs={"id": self.don_toliver["id"]}),
            {"name": 2015},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_update_unknown_artist(self):
        artist_id = self.don_toliver["id"] + 1
        response = self.client.put(
            reverse("api-1.0:update_artist", kwargs={"id": artist_id}),
            {"name": "Chinx Drugz"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Artist with id = {artist_id} does not exist."
        )


class DeleteArtist(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.french_montana = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "French Montana"},
            content_type="application/json",
        ).json()

    def test_delete_artist_successful(self):
        self.client.delete(
            reverse("api-1.0:delete_artist", kwargs={"id": self.french_montana["id"]})
        )
        response = self.client.get(
            reverse("api-1.0:retrieve_artist", kwargs={"id": self.french_montana["id"]})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Artist with id = {self.french_montana["id"]} does not exist."
        )

    def test_delete_artist_status_code(self):
        response = self.client.delete(
            reverse("api-1.0:delete_artist", kwargs={"id": self.french_montana["id"]})
        )

        self.assertEqual(response.status_code, 204)

    def test_delete_artist_json_response(self):
        response = self.client.delete(
            reverse("api-1.0:delete_artist", kwargs={"id": self.french_montana["id"]})
        )

        self.assertEqual(response.content, b"")

    def test_delete_unknown_artist(self):
        artist_id = self.french_montana["id"] + 1
        response = self.client.delete(
            reverse("api-1.0:delete_artist", kwargs={"id": artist_id})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Artist with id = {artist_id} does not exist."
        )
