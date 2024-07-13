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


class RetrieveDisc(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.bone_thugs = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Bone Thugs-N-Harmony"},
            content_type="application/json",
        ).json()
        cls.the_art_of_war = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "artists": [cls.bone_thugs["id"]],
                "title": "The Art Of War",
                "release_date": "1997-07-29",
            },
            content_type="application/json",
        ).json()
        cls.world_war_1 = cls.client.post(
            reverse("api-1.0:create_disc"),
            {
                "album": cls.the_art_of_war["id"],
                "title": "World War 1",
                "number": 1,
            },
            content_type="application/json",
        ).json()

    def test_retrieve_disc_status_code(self):
        response = self.client.get(reverse("api-1.0:retrieve_disc", kwargs={"id": self.world_war_1["id"]}))

        self.assertEqual(response.status_code, 200)

    def test_retrieve_disc_json_response(self):
        response = self.client.get(reverse("api-1.0:retrieve_disc", kwargs={"id": self.world_war_1["id"]})).json()

        self.assertEqual(response["album"]["title"], "The Art Of War")
        self.assertEqual(response["title"], "World War 1")
        self.assertEqual(response["number"], 1)
        self.assertTrue(response["url"].endswith(f"/api/v1/discs/{response["id"]}"))
        self.assertIsNone(response["tracklist"])

    def test_retrieve_unknown_disc(self):
        disc_id = self.world_war_1["id"] + 1
        response = self.client.get(
            reverse("api-1.0:retrieve_disc", kwargs={"id": disc_id})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Disc with id = {disc_id} does not exist."
        )


class UpdateDisc(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.wutang_clan = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Wu-Tang Clan"},
            content_type="application/json",
        ).json()
        cls.wutang_forever = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "artists": [cls.wutang_clan["id"]],
                "title": "Wu-Tang Forever",
                "release_date": "1997-06-03",
            },
            content_type="application/json",
        ).json()
        cls.disc2 = cls.client.post(
            reverse("api-1.0:create_disc"),
            {
                "album": cls.wutang_forever["id"],
                "title": "Disc Two",
                "number": 2,
            },
            content_type="application/json",
        ).json()

    def test_update_disc_status_code(self):
        response = self.client.put(
            reverse("api-1.0:update_disc", kwargs={"id": self.disc2["id"]}),
            {
                "album": self.wutang_forever["id"],
                "title": "Disc 2",
                "number": 2,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

    def test_update_disc_json_response(self):
        response = self.client.put(
            reverse("api-1.0:update_disc", kwargs={"id": self.disc2["id"]}),
            {
                "album": self.wutang_forever["id"],
                "title": "Disc 2",
                "number": 2,
            },
            content_type="application/json",
        ).json()

        self.assertEqual(response["album"]["title"], "Wu-Tang Forever")
        self.assertEqual(response["title"], "Disc 2")
        self.assertEqual(response["number"], 2)
        self.assertTrue(response["url"].endswith(f"/api/v1/discs/{response["id"]}"))
        self.assertIsNone(response["tracklist"])

    def test_update_disc_with_extraneous_whitespace(self):
        response = self.client.put(
            reverse("api-1.0:update_disc", kwargs={"id": self.disc2["id"]}),
            {
                "album": self.wutang_forever["id"],
                "title": "       Disc 2",
                "number": 2,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Disc 2")

    def test_update_disc_with_extraneous_fields(self):
        response = self.client.put(
            reverse("api-1.0:update_disc", kwargs={"id": self.disc2["id"]}),
            {
                "album": self.wutang_forever["id"],
                "title": "Disc 2",
                "number": 2,
                "track_count": 16,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Disc 2")
        self.assertFalse("track_count" in response.json().keys())

    def test_update_disc_with_missing_required_fields(self):
        response = self.client.put(
            reverse("api-1.0:update_disc", kwargs={"id": self.disc2["id"]}),
            {
                "title": "Disc 2",
                "number": 2,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_update_disc_with_invalid_values(self):
        response = self.client.put(
            reverse("api-1.0:update_disc", kwargs={"id": self.disc2["id"]}),
            {
                "album": "Wu-Tang Forever",
                "title": "Disc 2",
                "number": 2,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_update_unknown_disc(self):
        disc_id = self.disc2["id"] + 1
        response = self.client.put(
            reverse("api-1.0:update_disc", kwargs={"id": disc_id}),
            {
                "album": self.wutang_forever["id"],
                "title": "Disc 1",
                "number": 1,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Disc with id = {disc_id} does not exist."
        )
