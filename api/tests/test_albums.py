# from django.test import TestCase, Client
# from django.db import IntegrityError
# from django.urls import reverse


# class CreateAlbum(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.client = Client()
#         cls.travis_scott = cls.client.post(
#             reverse("api-1.0:create_artist"),
#             {"name": "Travis Scott"},
#             content_type="application/json",
#         ).json()

#     def test_create_valid_album_status_code(self):
#         response = self.client.post(
#             reverse("api-1.0:create_album"),
#             {
#                 "artists": [self.travis_scott["id"]],
#                 "title": "Rodeo",
#                 "release_date": "2015-09-04",
#                 "single": False,
#                 "multidisc": False,
#             },
#             content_type="application/json",
#         )

#         self.assertEqual(response.status_code, 201)

#     def test_create_valid_album_json_response(self):
#         response = self.client.post(
#             reverse("api-1.0:create_album"),
#             {
#                 "artists": [self.travis_scott["id"]],
#                 "title": "Rodeo",
#                 "release_date": "2015-09-04",
#                 "single": False,
#                 "multidisc": False,
#             },
#             content_type="application/json",
#         ).json()

#         self.assertEqual(len(response["artists"]), 1)
#         self.assertEqual(response["artists"][0]["name"], "Travis Scott")
#         self.assertEqual(response["title"], "Rodeo")
#         self.assertEqual(response["release_date"], "2015-09-04")
#         self.assertFalse(response["single"])
#         self.assertFalse(response["multidisc"])
#         self.assertTrue(response["url"].endswith(f"/api/v1/albums/{response["id"]}"))
#         self.assertIsNone(response["tracklist"])
#         self.assertIsNone(response["discs"])

#     def test_create_album_without_optional_fields_status_code(self):
#         response = self.client.post(
#             reverse("api-1.0:create_album"),
#             {
#                 "artists": [self.travis_scott["id"]],
#                 "title": "Birds In The Trap Sing McKnight",
#                 "release_date": "2016-09-02",
#             },
#             content_type="application/json",
#         )

#         self.assertEqual(response.status_code, 201)

#     def test_create_album_without_optional_fields_json_response(self):
#         response = self.client.post(
#             reverse("api-1.0:create_album"),
#             {
#                 "artists": [self.travis_scott["id"]],
#                 "title": "Birds In The Trap Sing McKnight",
#                 "release_date": "2016-09-02",
#             },
#             content_type="application/json",
#         ).json()

#         self.assertEqual(len(response["artists"]), 1)
#         self.assertEqual(response["artists"][0]["name"], "Travis Scott")
#         self.assertEqual(response["title"], "Birds In The Trap Sing McKnight")
#         self.assertEqual(response["release_date"], "2016-09-02")
#         self.assertFalse(response["single"])
#         self.assertFalse(response["multidisc"])
#         self.assertTrue(response["url"].endswith(f"/api/v1/albums/{response["id"]}"))
#         self.assertIsNone(response["tracklist"])
#         self.assertIsNone(response["discs"])

#     def test_create_album_with_extraneous_whitespace(self):
#         response = self.client.post(
#             reverse("api-1.0:create_album"),
#             {
#                 "artists": [self.travis_scott["id"]],
#                 "title": "   Astroworld   ",
#                 "release_date": "2018-08-03",
#             },
#             content_type="application/json",
#         )

#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json()["title"], "Astroworld")

#     def test_create_album_with_extraneous_fields(self):
#         response = self.client.post(
#             reverse("api-1.0:create_album"),
#             {
#                 "artists": [self.travis_scott["id"]],
#                 "title": "Utopia",
#                 "release_date": "2016-09-02",
#                 "label": "Cactus Jack Records",
#             },
#             content_type="application/json",
#         )

#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json()["title"], "Utopia")
#         self.assertFalse("label" in response.json().keys())

#     def test_create_duplicate_album(self):
#         self.client.post(
#             reverse("api-1.0:create_album"),
#             {
#                 "artists": [self.travis_scott["id"]],
#                 "title": "Huncho Jack, Jack Huncho",
#                 "release_date": "2017-12-21",
#             },
#             content_type="application/json",
#         )

#         with self.assertRaises(IntegrityError):
#             self.client.post(
#                 reverse("api-1.0:create_album"),
#                 {
#                     "artists": [self.travis_scott["id"]],
#                     "title": "Huncho Jack, Jack Huncho",
#                     "release_date": "2017-12-21",
#                 },
#                 content_type="application/json",
#             )

#     def test_create_album_with_missing_required_fields(self):
#         response = self.client.post(
#             reverse("api-1.0:create_album"),
#             {"artists": [self.travis_scott["id"]], "title": "Owl Pharaoh"},
#             content_type="application/json",
#         )

#         self.assertEqual(response.status_code, 422)

#     def test_create_album_with_invalid_values(self):
#         response = self.client.post(
#             reverse("api-1.0:create_album"),
#             {
#                 "artists": [self.travis_scott["id"]],
#                 "title": 2008,
#                 "release_date": "1993-09-03",
#             },
#             content_type="application/json",
#         )

#         self.assertEqual(response.status_code, 422)


# class RetrieveAlbum(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.client = Client()
#         cls.schoolboy_q = cls.client.post(
#             reverse("api-1.0:create_artist"),
#             {"name": "Schoolboy Q"},
#             content_type="application/json",
#         ).json()
#         cls.oxymoron = cls.client.post(
#             reverse("api-1.0:create_album"),
#             {
#                 "artists": [cls.schoolboy_q["id"]],
#                 "title": "Oxymoron",
#                 "release_date": "2014-02-25",
#             },
#             content_type="application/json",
#         ).json()

#     def test_retrieve_album_status_code(self):
#         response = self.client.get(
#             reverse("api-1.0:retrieve_album", kwargs={"id": self.oxymoron["id"]})
#         )

#         self.assertEqual(response.status_code, 200)

#     def test_retrieve_album_json_response(self):
#         response = self.client.get(
#             reverse("api-1.0:retrieve_album", kwargs={"id": self.oxymoron["id"]})
#         ).json()

#         self.assertEqual(len(response["artists"]), 1)
#         self.assertEqual(response["artists"][0]["name"], "Schoolboy Q")
#         self.assertEqual(response["title"], "Oxymoron")
#         self.assertEqual(response["release_date"], "2014-02-25")
#         self.assertFalse(response["single"])
#         self.assertFalse(response["multidisc"])
#         self.assertTrue(response["url"].endswith(f"/api/v1/albums/{self.oxymoron["id"]}"))
#         self.assertIsNone(response["tracklist"])
#         self.assertIsNone(response["discs"])

#     def test_retrieve_unknown_album(self):
#         album_id = self.oxymoron["id"] + 1
#         response = self.client.get(
#             reverse("api-1.0:retrieve_album", kwargs={"id": album_id})
#         )

#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(
#             response.json()["error"], f"Album with id = {album_id} does not exist."
#         )


# class UpdateAlbum(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.client = Client()
#         cls.freddie_gibbs = cls.client.post(
#             reverse("api-1.0:create_artist"),
#             {"name": "Freddie Gibbs"},
#             content_type="application/json",
#         ).json()
#         cls.alfredo = cls.client.post(
#             reverse("api-1.0:create_album"),
#             {
#                 "artists": [cls.freddie_gibbs["id"]],
#                 "title": "Alfredo",
#                 "release_date": "2020-05-29",
#             },
#             content_type="application/json",
#         ).json()

#     def test_update_album_status_code(self):
#         the_alchemist = self.client.post(
#             reverse("api-1.0:create_artist"),
#             {"name": "The Alchemist"},
#             content_type="application/json",
#         ).json()
#         response = self.client.put(
#             reverse("api-1.0:update_album", kwargs={"id": self.alfredo["id"]}),
#             {
#                 "artists": [self.freddie_gibbs["id"], the_alchemist["id"]],
#                 "title": "Alfredo",
#                 "release_date": "2020-05-29",
#             },
#             content_type="application/json",
#         )

#         self.assertEqual(response.status_code, 200)

#     def test_update_album_json_response(self):
#         the_alchemist = self.client.post(
#             reverse("api-1.0:create_artist"),
#             {"name": "The Alchemist"},
#             content_type="application/json",
#         ).json()
#         response = self.client.put(
#             reverse("api-1.0:update_album", kwargs={"id": self.alfredo["id"]}),
#             {
#                 "artists": [self.freddie_gibbs["id"], the_alchemist["id"]],
#                 "title": "Alfredo",
#                 "release_date": "2020-05-29",
#             },
#             content_type="application/json",
#         ).json()

#         self.assertEqual(len(response["artists"]), 2)
#         self.assertEqual(response["artists"][0]["name"], "Freddie Gibbs")
#         self.assertEqual(response["artists"][1]["name"], "The Alchemist")
#         self.assertEqual(response["title"], "Alfredo")
#         self.assertEqual(response["release_date"], "2020-05-29")
#         self.assertFalse(response["single"])
#         self.assertFalse(response["multidisc"])
#         self.assertTrue(response["url"].endswith(f"/api/v1/albums/{self.alfredo["id"]}"))
#         self.assertIsNone(response["tracklist"])
#         self.assertIsNone(response["discs"])

#     def test_update_album_with_extraneous_whitespace(self):
#         response = self.client.put(
#             reverse("api-1.0:update_album", kwargs={"id": self.alfredo["id"]}),
#             {
#                 "artists": [self.freddie_gibbs["id"]],
#                 "title": "    AlFredo    ",
#                 "release_date": "2020-05-29",
#             },
#             content_type="application/json",
#         )

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()["title"], "AlFredo")

#     def test_update_album_with_extraneous_fields(self):
#         response = self.client.put(
#             reverse("api-1.0:update_album", kwargs={"id": self.alfredo["id"]}),
#             {
#                 "artists": [self.freddie_gibbs["id"]],
#                 "title": "AlFredo",
#                 "release_date": "2020-05-29",
#                 "label": "ALC Records",
#             },
#             content_type="application/json",
#         )

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()["title"], "AlFredo")
#         self.assertFalse("label" in response.json().keys())

#     def test_update_album_with_missing_required_fields(self):
#         response = self.client.put(
#             reverse("api-1.0:update_album", kwargs={"id": self.alfredo["id"]}),
#             {
#                 "title": "AlFredo",
#                 "label": "ALC Records",
#             },
#             content_type="application/json",
#         )

#         self.assertEqual(response.status_code, 422)

#     def test_update_album_with_invalid_values(self):
#         response = self.client.put(
#             reverse("api-1.0:update_album", kwargs={"id": self.alfredo["id"]}),
#             {
#                 "artists": ["Freddie Gibbs", "The Alchemist"],
#                 "title": "AlFredo",
#                 "release_date": "2020-05-29",
#             },
#             content_type="application/json",
#         )

#         self.assertEqual(response.status_code, 422)

#     def test_update_unknown_album(self):
#         album_id = self.alfredo["id"] + 1
#         response = self.client.put(
#             reverse("api-1.0:update_album", kwargs={"id": album_id}),
#             {
#                 "artists": [self.freddie_gibbs["id"]],
#                 "title": "You Only Live 2wice",
#                 "release_date": "2017-03-31",
#             },
#             content_type="application/json",
#         )

#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(
#             response.json()["error"], f"Album with id = {album_id} does not exist."
#         )


# class DeleteAlbum(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.client = Client()
#         cls.prodigy = cls.client.post(
#             reverse("api-1.0:create_artist"),
#             {"name": "Prodigy"},
#             content_type="application/json",
#         ).json()
#         cls.albert_einstein = cls.client.post(
#             reverse("api-1.0:create_album"),
#             {
#                 "artists": [cls.prodigy["id"]],
#                 "title": "Albert Einstein",
#                 "release_date": "2013-06-11",
#             },
#             content_type="application/json",
#         ).json()

#     def test_delete_album_successful(self):
#         self.client.delete(
#             reverse("api-1.0:delete_album", kwargs={"id": self.albert_einstein["id"]})
#         )
#         response = self.client.get(
#             reverse("api-1.0:retrieve_album", kwargs={"id": self.albert_einstein["id"]})
#         )

#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(
#             response.json()["error"], f"Album with id = {self.albert_einstein["id"]} does not exist."
#         )

#     def test_delete_album_status_code(self):
#         response = self.client.delete(
#             reverse("api-1.0:delete_album", kwargs={"id": self.albert_einstein["id"]})
#         )

#         self.assertEqual(response.status_code, 204)

#     def test_delete_album_json_response(self):
#         response = self.client.delete(
#             reverse("api-1.0:delete_album", kwargs={"id": self.albert_einstein["id"]})
#         )

#         self.assertEqual(response.content, b"")

#     def test_delete_unknown_album(self):
#         album_id = self.albert_einstein["id"] + 1
#         response = self.client.delete(
#             reverse("api-1.0:delete_album", kwargs={"id": album_id})
#         )

#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(
#             response.json()["error"], f"Album with id = {album_id} does not exist."
#         )
