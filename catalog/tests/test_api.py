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


class RetrieveArtistTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.artist = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Tinashe"},
            content_type="application/json",
        ).json()

    def test_retrieve_artist(self):
        artist_id = self.artist["id"]
        response = self.client.get(
            reverse("api-1.0:retrieve_artist", kwargs={"id": artist_id})
        )

        self.assertEqual(response.status_code, 200)

        response = response.json()

        self.assertEqual(response["name"], "Tinashe")
        self.assertTrue(response["url"].endswith(f"/api/v1/artists/{artist_id}"))
        self.assertIsNone(response["albums"])
        self.assertIsNone(response["singles"])
        self.assertIsNone(response["songs"])
        self.assertIsNone(response["songs_produced"])

    def test_retrieve_unknown_artist(self):
        artist_id = self.artist["id"] + 1
        response = self.client.get(
            reverse("api-1.0:retrieve_artist", kwargs={"id": artist_id})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Artist with id = {artist_id} does not exist."
        )


class UpdateArtistTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.artist = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Chinx"},
            content_type="application/json",
        ).json()

    def test_update_artist(self):
        response = self.client.put(
            reverse("api-1.0:update_artist", kwargs={"id": self.artist["id"]}),
            {"name": "Chinx Drugz"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        response = response.json()
        artist_id = response["id"]

        self.assertEqual(self.artist["id"], artist_id)
        self.assertEqual(response["name"], "Chinx Drugz")
        self.assertTrue(response["url"].endswith(f"/api/v1/artists/{artist_id}"))
        self.assertIsNone(response["albums"])
        self.assertIsNone(response["singles"])
        self.assertIsNone(response["songs"])
        self.assertIsNone(response["songs_produced"])

    def test_update_artist_with_extraneous_whitespace(self):
        response = self.client.put(
            reverse("api-1.0:update_artist", kwargs={"id": self.artist["id"]}),
            {"name": "   Chinx Drugz   "},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Chinx Drugz")

    def test_update_artist_with_extraneous_fields(self):
        response = self.client.put(
            reverse("api-1.0:update_artist", kwargs={"id": self.artist["id"]}),
            {"name": "Chinx Drugz", "alias": "Chinx"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Chinx Drugz")
        self.assertFalse("alias" in response.json().keys())

    def test_update_artist_with_missing_required_fields(self):
        response = self.client.put(
            reverse("api-1.0:update_artist", kwargs={"id": self.artist["id"]}),
            {"label": "Def Jam Recordings"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_update_artist_with_invalid_values(self):
        response = self.client.put(
            reverse("api-1.0:update_artist", kwargs={"id": self.artist["id"]}),
            {"name": 42},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_update_unknown_artist(self):
        artist_id = self.artist["id"] + 1
        response = self.client.put(
            reverse("api-1.0:update_artist", kwargs={"id": artist_id}),
            {"name": "Chinx Drugz"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Artist with id = {artist_id} does not exist."
        )


class DeleteArtistTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.artist = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "French Montana"},
            content_type="application/json",
        ).json()

    def test_delete_artist(self):
        artist_id = self.artist["id"]
        response = self.client.delete(
            reverse("api-1.0:delete_artist", kwargs={"id": artist_id})
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")

        response = self.client.get(
            reverse("api-1.0:retrieve_artist", kwargs={"id": artist_id})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Artist with id = {artist_id} does not exist."
        )

    def test_delete_unknown_artist(self):
        artist_id = self.artist["id"] + 1
        response = self.client.delete(
            reverse("api-1.0:delete_artist", kwargs={"id": artist_id})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Artist with id = {artist_id} does not exist."
        )


class CreateAlbumTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.artist = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Travis Scott"},
            content_type="application/json",
        ).json()

    def test_create_album(self):
        response = self.client.post(
            reverse("api-1.0:create_album"),
            {
                "artists": [self.artist["id"]],
                "title": "Rodeo",
                "release_date": "2015-09-04",
                "single": False,
                "multidisc": False,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

        response = response.json()
        album_id = response["id"]

        self.assertEqual(response["album_artists"][0]["name"], "Travis Scott")
        self.assertEqual(response["title"], "Rodeo")
        self.assertEqual(response["release_date"], "2015-09-04")
        self.assertIsNone(response["tracklist"])
        self.assertFalse(response["single"])
        self.assertFalse(response["multidisc"])
        self.assertIsNone(response["discs"])
        self.assertTrue(response["url"].endswith(f"/api/v1/albums/{album_id}"))

    def test_create_album_without_optional_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_album"),
            {
                "artists": [self.artist["id"]],
                "title": "Birds In The Trap Sing McKnight",
                "release_date": "2016-09-02",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

        response = response.json()

        self.assertEqual(response["album_artists"][0]["name"], "Travis Scott")
        self.assertEqual(response["title"], "Birds In The Trap Sing McKnight")
        self.assertEqual(response["release_date"], "2016-09-02")
        self.assertFalse(response["single"])
        self.assertFalse(response["multidisc"])

    def test_create_album_with_extraneous_whitespace(self):
        response = self.client.post(
            reverse("api-1.0:create_album"),
            {
                "artists": [self.artist["id"]],
                "title": "   Astroworld   ",
                "release_date": "2018-08-03",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Astroworld")

    def test_create_album_with_extraneous_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_album"),
            {
                "artists": [self.artist["id"]],
                "title": "Utopia",
                "release_date": "2016-09-02",
                "label": "Cactus Jack Records",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Utopia")
        self.assertFalse("label" in response.json().keys())

    def test_create_duplicate_album(self):
        self.client.post(
            reverse("api-1.0:create_album"),
            {
                "artists": [self.artist["id"]],
                "title": "Huncho Jack, Jack Huncho",
                "release_date": "2017-12-21",
            },
            content_type="application/json",
        )

        with self.assertRaises(IntegrityError):
            self.client.post(
                reverse("api-1.0:create_album"),
                {
                    "artists": [self.artist["id"]],
                    "title": "Huncho Jack, Jack Huncho",
                    "release_date": "2017-12-21",
                },
                content_type="application/json",
            )

    def test_create_album_with_missing_required_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_album"),
            {"artists": [self.artist["id"]], "title": "Owl Pharaoh"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_create_album_with_invalid_values(self):
        response = self.client.post(
            reverse("api-1.0:create_album"),
            {
                "artists": [self.artist["id"]],
                "title": 42,
                "release_date": "1993-09-03",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)
