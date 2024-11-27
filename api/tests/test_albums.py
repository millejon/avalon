from django.test import TestCase, Client
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
