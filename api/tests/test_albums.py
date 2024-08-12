from django.test import TestCase, Client
from django.urls import reverse


class CreateAlbumTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_create_valid_album_status_code(self):
        response = self.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "The Infamous",
                "release_date": "1995-04-25",
                "single": False,
                "multidisc": False,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_album_json_response(self):
        response = self.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "The Infamous",
                "release_date": "1995-04-25",
            },
            content_type="application/json",
        ).json()

        self.assertEqual(response["title"], "The Infamous")
        self.assertEqual(len(response["artists"]), 0)
        self.assertIsNone(response["tracklist"])
        self.assertEqual(response["release_date"], "1995-04-25")
        self.assertFalse(response["single"])
        self.assertFalse(response["multidisc"])
        self.assertIsNone(response["discs"])
        self.assertTrue(response["url"].endswith(f"/api/v1/albums/{response["id"]}"))

    def test_create_valid_multidisc_album_status_code(self):
        response = self.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "Life After Death",
                "release_date": "1997-03-25",
                "single": False,
                "multidisc": True,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_multidisc_album_json_response(self):
        response = self.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "Life After Death",
                "release_date": "1997-03-25",
                "single": False,
                "multidisc": True,
            },
            content_type="application/json",
        ).json()

        self.assertEqual(response["title"], "Life After Death")
        self.assertEqual(len(response["artists"]), 0)
        self.assertIsNone(response["tracklist"])
        self.assertEqual(response["release_date"], "1997-03-25")
        self.assertFalse(response["single"])
        self.assertTrue(response["multidisc"])
        self.assertEqual(response["discs"]["count"], 0)
        self.assertTrue(response["discs"]["url"].endswith(f"/api/v1/albums/{response["id"]}/discs"))
        self.assertTrue(response["url"].endswith(f"/api/v1/albums/{response["id"]}"))

    def test_create_album_with_extraneous_whitespace(self):
        response = self.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "   Reasonable Doubt   ",
                "release_date": "1996-06-25",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Reasonable Doubt")

    def test_create_album_with_extraneous_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "Only Built 4 Cuban Linx",
                "release_date": "1995-08-01",
                "label": "Loud Records",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Only Built 4 Cuban Linx")
        self.assertFalse("label" in response.json().keys())

    def test_create_duplicate_album(self):
        album_metadata = {
            "title": "It's Dark and Hell Is Hot",
            "release_date": "1998-05-19",
        }
        self.client.post(
            reverse("api-1.0:create_album"),
            album_metadata,
            content_type="application/json",
        )
        response = self.client.post(
            reverse("api-1.0:create_album"),
            album_metadata,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Album already exists in database.")

    def test_create_multidisc_single(self):
        response = self.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "Déjà Vu (Uptown Baby)",
                "release_date": "1997-12-09",
                "single": True,
                "multidisc": True,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Singles can not be multidisc.")

    def test_create_album_with_missing_required_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_album"),
            {"title": "The War Report"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_create_album_with_invalid_values(self):
        response = self.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": 456,
                "release_date": "1995-09-26",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)


class RetrieveAlbumTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.venni_vetti_vecci = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "Venni Vetti Vecci",
                "release_date": "1999-06-01",
            },
            content_type="application/json",
        ).json()

    def test_retrieve_album_status_code(self):
        response = self.client.get(
            reverse("api-1.0:retrieve_album", kwargs={"id": self.venni_vetti_vecci["id"]})
        )

        self.assertEqual(response.status_code, 200)

    def test_retrieve_album_json_response(self):
        response = self.client.get(
            reverse("api-1.0:retrieve_album", kwargs={"id": self.venni_vetti_vecci["id"]})
        ).json()

        self.assertEqual(response["id"], self.venni_vetti_vecci["id"])
        self.assertEqual(response["title"], "Venni Vetti Vecci")
        self.assertEqual(len(response["artists"]), 0)
        self.assertIsNone(response["tracklist"])
        self.assertEqual(response["release_date"], "1999-06-01")
        self.assertFalse(response["single"])
        self.assertFalse(response["multidisc"])
        self.assertIsNone(response["discs"])
        self.assertTrue(response["url"].endswith(f"/api/v1/albums/{self.venni_vetti_vecci["id"]}"))

    def test_retrieve_unknown_album(self):
        album_id = self.venni_vetti_vecci["id"] + 100
        response = self.client.get(
            reverse("api-1.0:retrieve_album", kwargs={"id": album_id})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Album with id = {album_id} does not exist."
        )


class UpdateAlbum(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.freddie_gibbs = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Freddie Gibbs"},
            content_type="application/json",
        ).json()
        cls.alfredo = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "artists": [cls.freddie_gibbs["id"]],
                "title": "Alfredo",
                "release_date": "2020-05-29",
            },
            content_type="application/json",
        ).json()

    def test_update_album_status_code(self):
        the_alchemist = self.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "The Alchemist"},
            content_type="application/json",
        ).json()
        response = self.client.put(
            reverse("api-1.0:update_album", kwargs={"id": self.alfredo["id"]}),
            {
                "artists": [self.freddie_gibbs["id"], the_alchemist["id"]],
                "title": "Alfredo",
                "release_date": "2020-05-29",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

    def test_update_album_json_response(self):
        the_alchemist = self.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "The Alchemist"},
            content_type="application/json",
        ).json()
        response = self.client.put(
            reverse("api-1.0:update_album", kwargs={"id": self.alfredo["id"]}),
            {
                "artists": [self.freddie_gibbs["id"], the_alchemist["id"]],
                "title": "Alfredo",
                "release_date": "2020-05-29",
            },
            content_type="application/json",
        ).json()

        self.assertEqual(len(response["artists"]), 2)
        self.assertEqual(response["artists"][0]["name"], "Freddie Gibbs")
        self.assertEqual(response["artists"][1]["name"], "The Alchemist")
        self.assertEqual(response["title"], "Alfredo")
        self.assertEqual(response["release_date"], "2020-05-29")
        self.assertFalse(response["single"])
        self.assertFalse(response["multidisc"])
        self.assertTrue(response["url"].endswith(f"/api/v1/albums/{self.alfredo["id"]}"))
        self.assertIsNone(response["tracklist"])
        self.assertIsNone(response["discs"])

    def test_update_album_with_extraneous_whitespace(self):
        response = self.client.put(
            reverse("api-1.0:update_album", kwargs={"id": self.alfredo["id"]}),
            {
                "artists": [self.freddie_gibbs["id"]],
                "title": "    AlFredo    ",
                "release_date": "2020-05-29",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "AlFredo")

    def test_update_album_with_extraneous_fields(self):
        response = self.client.put(
            reverse("api-1.0:update_album", kwargs={"id": self.alfredo["id"]}),
            {
                "artists": [self.freddie_gibbs["id"]],
                "title": "AlFredo",
                "release_date": "2020-05-29",
                "label": "ALC Records",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "AlFredo")
        self.assertFalse("label" in response.json().keys())

    def test_update_album_with_missing_required_fields(self):
        response = self.client.put(
            reverse("api-1.0:update_album", kwargs={"id": self.alfredo["id"]}),
            {
                "title": "AlFredo",
                "label": "ALC Records",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_update_album_with_invalid_values(self):
        response = self.client.put(
            reverse("api-1.0:update_album", kwargs={"id": self.alfredo["id"]}),
            {
                "artists": ["Freddie Gibbs", "The Alchemist"],
                "title": "AlFredo",
                "release_date": "2020-05-29",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_update_unknown_album(self):
        album_id = self.alfredo["id"] + 1
        response = self.client.put(
            reverse("api-1.0:update_album", kwargs={"id": album_id}),
            {
                "artists": [self.freddie_gibbs["id"]],
                "title": "You Only Live 2wice",
                "release_date": "2017-03-31",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Album with id = {album_id} does not exist."
        )


class DeleteAlbum(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.prodigy = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Prodigy"},
            content_type="application/json",
        ).json()
        cls.albert_einstein = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "artists": [cls.prodigy["id"]],
                "title": "Albert Einstein",
                "release_date": "2013-06-11",
            },
            content_type="application/json",
        ).json()

    def test_delete_album_successful(self):
        self.client.delete(
            reverse("api-1.0:delete_album", kwargs={"id": self.albert_einstein["id"]})
        )
        response = self.client.get(
            reverse("api-1.0:retrieve_album", kwargs={"id": self.albert_einstein["id"]})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Album with id = {self.albert_einstein["id"]} does not exist."
        )

    def test_delete_album_status_code(self):
        response = self.client.delete(
            reverse("api-1.0:delete_album", kwargs={"id": self.albert_einstein["id"]})
        )

        self.assertEqual(response.status_code, 204)

    def test_delete_album_json_response(self):
        response = self.client.delete(
            reverse("api-1.0:delete_album", kwargs={"id": self.albert_einstein["id"]})
        )

        self.assertEqual(response.content, b"")

    def test_delete_unknown_album(self):
        album_id = self.albert_einstein["id"] + 1
        response = self.client.delete(
            reverse("api-1.0:delete_album", kwargs={"id": album_id})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Album with id = {album_id} does not exist."
        )
