from django.test import TestCase, Client
from django.urls import reverse


class CreateSongTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.aquemini = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "Aquemini",
                "release_date": "1998-09-29",
            },
            content_type="application/json",
        ).json()
        cls.speakerboxxx_the_love_below = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "Speakerboxxx / The Love Below",
                "release_date": "2003-09-23",
                "multidisc": True,
            },
            content_type="application/json",
        ).json()

    def test_create_valid_song_status_code(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Rosa Parks",
                "album": self.aquemini["id"],
                "track_number": 3,
                "length": 324,
                "path": "/outkast/aquemini/03_rosa_parks.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_song_json_response(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Rosa Parks",
                "album": self.aquemini["id"],
                "track_number": 3,
                "length": 324,
                "path": "/outkast/aquemini/03_rosa_parks.flac",
            },
            content_type="application/json",
        ).json()

        self.assertEqual(response["title"], "Rosa Parks")
        self.assertEqual(len(response["artists"]), 0)
        self.assertEqual(len(response["producers"]), 0)
        self.assertEqual(response["album"]["title"], "Aquemini")
        self.assertIsNone(response["disc"])
        self.assertEqual(response["track_number"], 3)
        self.assertEqual(response["length"], 324)
        self.assertEqual(response["path"], "/outkast/aquemini/03_rosa_parks.flac")
        self.assertEqual(response["play_count"], 0)
        self.assertTrue(response["url"].endswith(f"/api/v1/songs/{response["id"]}"))

    def test_create_valid_multidisc_song_status_code(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Flip Flop Rock",
                "album": self.speakerboxxx_the_love_below["id"],
                "disc": 1,
                "track_number": 14,
                "length": 276,
                "path": "/outkast/speakerboxx-the-love-below/speakerboxx/11_flip_flop_rock.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_multidisc_song_json_response(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Flip Flop Rock",
                "album": self.speakerboxxx_the_love_below["id"],
                "disc": 1,
                "track_number": 14,
                "length": 276,
                "path": "/outkast/speakerboxx-the-love-below/speakerboxx/11_flip_flop_rock.flac",
            },
            content_type="application/json",
        ).json()

        self.assertEqual(response["title"], "Flip Flop Rock")
        self.assertEqual(len(response["artists"]), 0)
        self.assertEqual(len(response["producers"]), 0)
        self.assertEqual(response["album"]["title"], "Speakerboxxx / The Love Below")
        self.assertEqual(response["disc"], 1)
        self.assertEqual(response["track_number"], 14)
        self.assertEqual(response["length"], 276)
        self.assertEqual(response["path"], "/outkast/speakerboxx-the-love-below/speakerboxx/11_flip_flop_rock.flac")
        self.assertEqual(response["play_count"], 0)
        self.assertTrue(response["url"].endswith(f"/api/v1/songs/{response["id"]}"))

    def test_create_song_with_extraneous_whitespace(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "       Skew It On The Bar-B     ",
                "album": self.aquemini["id"],
                "track_number": 4,
                "length": 195,
                "path": "/outkast/aquemini/04_skew_it_on_the_barb.flac       ",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Skew It On The Bar-B")
        self.assertEqual(response.json()["path"], "/outkast/aquemini/04_skew_it_on_the_barb.flac")

    def test_create_song_with_extraneous_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Synthesizer",
                "album": self.aquemini["id"],
                "track_number": 6,
                "length": 311,
                "path": "/outkast/aquemini/06_synthesizer.flac",
                "writers": ["Antwan Patton", "André Benjamin", "George Clinton"],
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Synthesizer")
        self.assertFalse("writers" in response.json().keys())

    def test_create_song_with_unknown_album(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "B.O.B.",
                "album": self.aquemini["id"] + 100,
                "track_number": 11,
                "length": 304,
                "path": "/outkast/stankonia/11_bob.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Album with id = {self.aquemini["id"] + 100} does not exist."
        )

    def test_create_song_with_invalid_disc_number(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Last Call",
                "album": self.speakerboxxx_the_love_below["id"],
                "disc": -1,
                "track_number": 18,
                "length": 238,
                "path": "/outkast/speakerboxx-the-love-below/speakerboxx/18_last_call.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        message = ("There is something wrong with the data submitted. Please "
                   "consult the API documentation and try again.")
        self.assertEqual(response.json()["error"], message)

    def test_create_song_with_invalid_track_number(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Da Art Of Storytellin', Pt. 1",
                "album": self.aquemini["id"],
                "track_number": -9,
                "length": 223,
                "path": "/outkast/aquemini/09_da_art_of_storytellin_pt_1.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        message = ("There is something wrong with the data submitted. Please "
                   "consult the API documentation and try again.")
        self.assertEqual(response.json()["error"], message)

    def test_create_duplicate_song(self):
        song_metadata = {
            "title": "Da Art Of Storytellin', Pt. 2",
            "album": self.aquemini["id"],
            "track_number": 10,
            "length": 168,
            "path": "/outkast/aquemini/10_da_art_of_storytellin_pt_2.flac",
        }
        self.client.post(reverse("api-1.0:create_song"), song_metadata, content_type="application/json")
        response = self.client.post(reverse("api-1.0:create_song"), song_metadata, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Song already exists in database.")

    def test_create_song_with_missing_required_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Mamacita",
                "album": self.aquemini["id"],
                "track_number": 11,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_create_song_with_invalid_values(self):
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Chonkyfire",
                "album": "Aquemini",
                "track_number": 16,
                "length": 370,
                "path": "/outkast/aquemini/16_chonkyfire.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)


class RetrieveSongTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.ridin_dirty = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "Ridin' Dirty",
                "release_date": "1996-07-30",
            },
            content_type="application/json",
        ).json()
        cls.hilife = cls.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Hi-Life",
                "album": cls.ridin_dirty["id"],
                "track_number": 10,
                "length": 325,
                "path": "/ugk/ridin-dirty/10_hilife.flac",
            },
            content_type="application/json",
        ).json()

    def test_retrieve_song_status_code(self):
        response = self.client.get(
            reverse("api-1.0:retrieve_song", kwargs={"id": self.hilife["id"]})
        )

        self.assertEqual(response.status_code, 200)

    def test_retrieve_song_json_response(self):
        response = self.client.get(
            reverse("api-1.0:retrieve_song", kwargs={"id": self.hilife["id"]})
        ).json()

        self.assertEqual(response["id"], self.hilife["id"])
        self.assertEqual(response["title"], "Hi-Life")
        self.assertEqual(len(response["artists"]), 0)
        self.assertEqual(len(response["producers"]), 0)
        self.assertEqual(response["album"]["title"], "Ridin' Dirty")
        self.assertIsNone(response["disc"])
        self.assertEqual(response["track_number"], 10)
        self.assertEqual(response["length"], 325)
        self.assertEqual(response["path"], "/ugk/ridin-dirty/10_hilife.flac")
        self.assertEqual(response["play_count"], 0)
        self.assertTrue(response["url"].endswith(f"/api/v1/songs/{self.hilife["id"]}"))

    def test_retrieve_unknown_song(self):
        song_id = self.hilife["id"] + 100
        response = self.client.get(
            reverse("api-1.0:retrieve_song", kwargs={"id": song_id})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Song with id = {song_id} does not exist."
        )


class UpdateSongTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.my_homies = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "My Homies",
                "release_date": "1998-03-03",
                "multidisc": True,
            },
            content_type="application/json",
        ).json()
        cls.disc1 = cls.client.post(
            reverse("api-1.0:create_disc"),
            {
                "album": cls.my_homies["id"],
                "title": "Disc 1",
                "number": 1,
            },
            content_type="application/json",
        ).json()
        cls.win_lose_or_draw = cls.client.post(
            reverse("api-1.0:create_song"),
            {
                "album": cls.my_homies["id"],
                "title": "Win Lose or Draw",
                "track_number": 12,
                "length": 316,
                "path": "/scarface/my-homies/disc-1/12_win_lose_or_draw.flac",
            },
            content_type="application/json",
        ).json()

    def test_update_song_status_code(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.win_lose_or_draw["id"]}),
            {
                "album": self.my_homies["id"],
                "title": "Win, Lose, or Draw",
                "track_number": 12,
                "length": 316,
                "path": "/scarface/my-homies/disc-1/12_win_lose_or_draw.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

    def test_update_song_json_response(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.win_lose_or_draw["id"]}),
            {
                "album": self.my_homies["id"],
                "disc": self.disc1["id"],
                "title": "Win, Lose, or Draw",
                "track_number": 12,
                "length": 316,
                "path": "/scarface/my-homies/disc-1/12_win_lose_or_draw.flac",
            },
            content_type="application/json",
        ).json()

        self.assertEqual(response["title"], "Win, Lose, or Draw")
        self.assertEqual(response["id"], self.win_lose_or_draw["id"])
        self.assertEqual(len(response["artists"]), 0)
        self.assertEqual(len(response["producers"]), 0)
        self.assertEqual(response["album"]["title"], "My Homies")
        self.assertEqual(response["disc"], 1)
        self.assertEqual(response["track_number"], 12)
        self.assertEqual(response["length"], 316)
        self.assertEqual(response["path"], "/scarface/my-homies/disc-1/12_win_lose_or_draw.flac")
        self.assertEqual(response["play_count"], 0)
        self.assertTrue(response["url"].endswith(f"/api/v1/songs/{self.win_lose_or_draw["id"]}"))

    def test_update_song_with_extraneous_whitespace(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.win_lose_or_draw["id"]}),
            {
                "album": self.my_homies["id"],
                "disc": self.disc1["id"],
                "title": "Win, Lose, or Draw      ",
                "track_number": 12,
                "length": 316,
                "path": "     /scarface/my-homies/disc-1/12_win_lose_or_draw.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Win, Lose, or Draw")
        self.assertEqual(response.json()["path"], "/scarface/my-homies/disc-1/12_win_lose_or_draw.flac")

    def test_update_song_with_extraneous_fields(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.win_lose_or_draw["id"]}),
            {
                "album": self.my_homies["id"],
                "disc": self.disc1["id"],
                "title": "Win, Lose, or Draw",
                "track_number": 12,
                "length": 316,
                "publisher": "N The Water Publishing, Inc.",
                "path": "/scarface/my-homies/disc-1/12_win_lose_or_draw.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Win, Lose, or Draw")
        self.assertFalse("publisher" in response.json().keys())

    def test_update_song_with_unknown_album(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.win_lose_or_draw["id"]}),
            {
                "album": self.my_homies["id"] + 100,
                "disc": self.disc1["id"],
                "title": "Win, Lose, or Draw",
                "track_number": 12,
                "length": 316,
                "publisher": "N The Water Publishing, Inc.",
                "path": "/scarface/my-homies/disc-1/12_win_lose_or_draw.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Album with id = {self.my_homies["id"] + 100} does not exist."
        )

    def test_update_song_with_unknown_disc(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.win_lose_or_draw["id"]}),
            {
                "album": self.my_homies["id"],
                "disc": self.disc1["id"] + 100,
                "title": "Win, Lose, or Draw",
                "track_number": 12,
                "length": 316,
                "publisher": "N The Water Publishing, Inc.",
                "path": "/scarface/my-homies/disc-1/12_win_lose_or_draw.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Disc with id = {self.disc1["id"] + 100} does not exist."
        )

    def test_update_song_with_missing_required_fields(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.win_lose_or_draw["id"]}),
            {
                "album": self.my_homies["id"],
                "title": "Win, Lose, or Draw",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_update_song_with_invalid_values(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.win_lose_or_draw["id"]}),
            {
                "album": "My Homies",
                "disc": "Disc 1",
                "title": "Win, Lose, or Draw",
                "track_number": 12,
                "length": 316,
                "path": "/scarface/my-homies/disc-1/12_win_lose_or_draw.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_update_unknown_song(self):
        song_id = self.win_lose_or_draw["id"] + 100
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": song_id}),
            {
                "album": self.my_homies["id"],
                "disc": self.disc1["id"],
                "title": "Overnight",
                "track_number": 13,
                "length": 249,
                "path": "/scarface/my-homies/disc-1/13_overnight.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Song with id = {song_id} does not exist."
        )


class DeleteSongTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.when_the_smoke_clears = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "When The Smoke Clears: Sixty 6, Sixty 1",
                "release_date": "2000-06-13",
            },
            content_type="application/json",
        ).json()
        cls.sippin_on_some_syrup = cls.client.post(
            reverse("api-1.0:create_song"),
            {
                "album": cls.when_the_smoke_clears["id"],
                "title": "Sippin' On Some Syrup",
                "track_number": 3,
                "length": 264,
                "path": "/three-6-mafia/when-the-smoke-clears-sixty-6-sixty-1/03_sippin_on_some_syrup.flac",
            },
            content_type="application/json",
        ).json()

    def test_delete_song_status_code(self):
        response = self.client.delete(
            reverse("api-1.0:delete_song", kwargs={"id": self.sippin_on_some_syrup["id"]})
        )

        self.assertEqual(response.status_code, 204)

    def test_delete_song_json_response(self):
        response = self.client.delete(
            reverse("api-1.0:delete_song", kwargs={"id": self.sippin_on_some_syrup["id"]})
        )

        self.assertFalse(response.content)

    def test_delete_song_successful(self):
        self.client.delete(
            reverse("api-1.0:delete_song", kwargs={"id": self.sippin_on_some_syrup["id"]})
        )
        response = self.client.get(
            reverse("api-1.0:retrieve_song", kwargs={"id": self.sippin_on_some_syrup["id"]})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Song with id = {self.sippin_on_some_syrup["id"]} does not exist."
        )

    def test_delete_unknown_song(self):
        song_id = self.sippin_on_some_syrup["id"] + 100
        response = self.client.delete(
            reverse("api-1.0:delete_song", kwargs={"id": song_id})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Song with id = {song_id} does not exist."
        )


class CreateSongFeatureTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.goodie_mob = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Goodie Mob"},
            content_type="application/json",
        ).json()
        cls.big_gipp = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Big Gipp"},
            content_type="application/json",
        ).json()
        cls.organized_noize = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Organized Noize"},
            content_type="application/json",
        ).json()
        cls.soul_food = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "Soul Food",
                "release_date": "1995-11-07",
            },
            content_type="application/json",
        ).json()
        cls.goodie_bag = cls.client.post(
            reverse("api-1.0:create_song"),
            {
                "album": cls.soul_food["id"],
                "title": "Goodie Bag",
                "track_number": 12,
                "length": 265,
                "path": "/goodie-mob/soul-food/12_goodie_bag.flac",
            },
            content_type="application/json",
        ).json()

    def test_create_valid_artist_song_feature_status_code(self):
        response = self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": self.goodie_bag["id"]}),
            {"artist": self.goodie_mob["id"]},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_artist_song_feature_json_response(self):
        response = self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": self.goodie_bag["id"]}),
            {"artist": self.goodie_mob["id"]},
            content_type="application/json",
        ).json()

        self.assertEqual(response["song"]["title"], "Goodie Bag")
        self.assertEqual(response["artist"]["name"], "Goodie Mob")
        self.assertFalse(response["group"])
        self.assertFalse(response["producer"])
        self.assertIsNone(response["role"])

    def test_create_valid_group_song_feature_status_code(self):
        response = self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": self.goodie_bag["id"]}),
            {
                "artist": self.big_gipp["id"],
                "group": True,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_group_song_feature_json_response(self):
        response = self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": self.goodie_bag["id"]}),
            {
                "artist": self.big_gipp["id"],
                "group": True,
            },
            content_type="application/json",
        ).json()

        self.assertEqual(response["song"]["title"], "Goodie Bag")
        self.assertEqual(response["artist"]["name"], "Big Gipp")
        self.assertTrue(response["group"])
        self.assertFalse(response["producer"])
        self.assertIsNone(response["role"])

    def test_create_valid_producer_song_feature_status_code(self):
        response = self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": self.goodie_bag["id"]}),
            {
                "artist": self.organized_noize["id"],
                "producer": True,
                "role": "Producer"
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_producer_song_feature_json_response(self):
        response = self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": self.goodie_bag["id"]}),
            {
                "artist": self.organized_noize["id"],
                "producer": True,
                "role": "Producer"
            },
            content_type="application/json",
        ).json()

        self.assertEqual(response["song"]["title"], "Goodie Bag")
        self.assertEqual(response["artist"]["name"], "Organized Noize")
        self.assertFalse(response["group"])
        self.assertTrue(response["producer"])
        self.assertEqual(response["role"], "Producer")

    def test_create_song_feature_with_extraneous_whitespace(self):
        response = self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": self.goodie_bag["id"]}),
            {
                "artist": self.organized_noize["id"],
                "producer": True,
                "role": "           Producer"
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["role"], "Producer")

    def test_create_song_feature_with_extraneous_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": self.goodie_bag["id"]}),
            {
                "artist": self.goodie_mob["id"],
                "hub": "dungeon_family"
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["artist"]["name"], "Goodie Mob")
        self.assertFalse("hub" in response.json().keys())

    def test_create_song_feature_with_unknown_song(self):
        response = self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": self.goodie_bag["id"] + 100}),
            {"artist": self.goodie_mob["id"]},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Song with id = {self.goodie_bag["id"] + 100} does not exist."
        )

    def test_create_song_feature_with_unknown_artist(self):
        response = self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": self.goodie_bag["id"]}),
            {"artist": self.goodie_mob["id"] + 100},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Artist with id = {self.goodie_mob["id"] + 100} does not exist."
        )

    def test_create_producer_song_feature_group_member(self):
        response = self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": self.goodie_bag["id"]}),
            {
                "artist": self.organized_noize["id"],
                "group": True,
                "producer": True,
                "role": "Producer"
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        message = ("There is something wrong with the data submitted. Please "
                   "consult the API documentation and try again.")
        self.assertEqual(response.json()["error"], message)

    def test_create_group_song_feature_with_role(self):
        response = self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": self.goodie_bag["id"]}),
            {
                "artist": self.big_gipp["id"],
                "group": True,
                "role": "Vocalist",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        message = ("There is something wrong with the data submitted. Please "
                   "consult the API documentation and try again.")
        self.assertEqual(response.json()["error"], message)

    def test_create_duplicate_artist_song_feature(self):
        song_id = self.goodie_bag["id"]
        self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": song_id}),
            {"artist": self.goodie_mob["id"]},
            content_type="application/json",
        )

        response = self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": song_id}),
            {
                "artist": self.goodie_mob["id"],
                "group": True
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        message = (f"Artist with id = {self.goodie_mob["id"]} is already "
                   f"credited as a song artist for song with id = {song_id}.")
        self.assertEqual(response.json()["error"], message)

    def test_create_duplicate_producer_song_feature(self):
        song_id = self.goodie_bag["id"]
        self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": self.goodie_bag["id"]}),
            {
                "artist": self.organized_noize["id"],
                "producer": True,
                "role": "Producer"
            },
            content_type="application/json",
        )

        response = self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": self.goodie_bag["id"]}),
            {
                "artist": self.organized_noize["id"],
                "producer": True,
                "role": "Additional Producer"
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        message = (f"Artist with id = {self.organized_noize["id"]} is already "
                   f"credited as a producer for song with id = {song_id}.")
        self.assertEqual(response.json()["error"], message)

    def test_create_song_feature_with_missing_required_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": self.goodie_bag["id"]}),
            {},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_create_song_feature_with_invalid_values(self):
        response = self.client.post(
            reverse("api-1.0:create_song_feature", kwargs={"id": self.goodie_bag["id"]}),
            {
                "artist": "Goodie Mob",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)
