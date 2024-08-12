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
                "path": "/outkast/aquemini/04_skew_it_on_the_bar-b.flac       ",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Skew It On The Bar-B")
        self.assertEqual(response.json()["path"], "/outkast/aquemini/04_skew_it_on_the_bar-b.flac")

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
        album_id = self.aquemini["id"] + 100
        response = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "B.O.B.",
                "album": album_id,
                "track_number": 11,
                "length": 304,
                "path": "/outkast/stankonia/11_bob.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Album with id = {album_id} does not exist."
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
        self.client.post(
            reverse("api-1.0:create_song"),
            song_metadata,
            content_type="application/json",
        )
        response = self.client.post(
            reverse("api-1.0:create_song"),
            song_metadata,
            content_type="application/json",
        )

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
        cls.ugk = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "U.G.K."},
            content_type="application/json",
        ).json()
        cls.pimp_c = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Pimp C"},
            content_type="application/json",
        ).json()
        cls.no_joe = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "N.O. Joe"},
            content_type="application/json",
        ).json()
        cls.ridin_dirty = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "Ridin' Dirty",
                "release_date": "1996-07-30",
            },
            content_type="application/json",
        ).json()
        cls.hi_life = cls.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Hi-Life",
                "album": cls.ridin_dirty["id"],
                "track_number": 10,
                "length": 325,
                "path": "/ugk/ridin-dirty/10_hi-life.flac",
            },
            content_type="application/json",
        ).json()

    def test_retrieve_song_status_code(self):
        response = self.client.get(
            reverse("api-1.0:retrieve_song", kwargs={"id": self.hi_life["id"]})
        )

        self.assertEqual(response.status_code, 200)

    def test_retrieve_song_json_response(self):
        response = self.client.get(
            reverse("api-1.0:retrieve_song", kwargs={"id": self.hi_life["id"]})
        ).json()

        self.assertEqual(response["id"], self.hi_life["id"])
        self.assertEqual(response["title"], "Hi-Life")
        self.assertEqual(len(response["artists"]), 0)
        self.assertEqual(len(response["producers"]), 0)
        self.assertEqual(response["album"]["title"], "Ridin' Dirty")
        self.assertIsNone(response["disc"])
        self.assertEqual(response["track_number"], 10)
        self.assertEqual(response["length"], 325)
        self.assertEqual(response["path"], "/ugk/ridin-dirty/10_hi-life.flac")
        self.assertEqual(response["play_count"], 0)
        self.assertTrue(response["url"].endswith(f"/api/v1/songs/{self.hi_life["id"]}"))

    def test_retrieve_song_json_response_only_shows_main_artists(self):
        self.client.post(
            reverse("api-1.0:create_song_artist", kwargs={"id": self.hi_life["id"]}),
            {"artist": self.ugk["id"]},
            content_type="application/json",
        )
        self.client.post(
            reverse("api-1.0:create_song_artist", kwargs={"id": self.hi_life["id"]}),
            {
                "artist": self.pimp_c["id"],
                "group": True,
            },
            content_type="application/json",
        )
        response = self.client.get(
            reverse("api-1.0:retrieve_song", kwargs={"id": self.hi_life["id"]})
        ).json()

        self.assertEqual(len(response["artists"]), 1)
        self.assertEqual(response["artists"][0]["id"], self.ugk["id"])
        self.assertEqual(response["artists"][0]["name"], "U.G.K.")
        self.assertTrue(response["artists"][0]["url"].endswith(f"/api/v1/artists/{self.ugk["id"]}"))

    def test_retrieve_song_json_response_only_shows_main_producers(self):
        self.client.post(
            reverse("api-1.0:create_song_producer", kwargs={"id": self.hi_life["id"]}),
            {
                "producer": self.no_joe["id"],
                "role": "Producer",
            },
            content_type="application/json",
        )
        self.client.post(
            reverse("api-1.0:create_song_producer", kwargs={"id": self.hi_life["id"]}),
            {
                "producer": self.pimp_c["id"],
                "role": "Co-Producer",
            },
            content_type="application/json",
        )
        response = self.client.get(
            reverse("api-1.0:retrieve_song", kwargs={"id": self.hi_life["id"]})
        ).json()

        self.assertEqual(len(response["producers"]), 1)
        self.assertEqual(response["producers"][0]["id"], self.no_joe["id"])
        self.assertEqual(response["producers"][0]["name"], "N.O. Joe")
        self.assertTrue(response["producers"][0]["url"].endswith(f"/api/v1/artists/{self.no_joe["id"]}"))

    def test_retrieve_unknown_song(self):
        song_id = self.hi_life["id"] + 100
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
        cls.the_diary = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "The Diary",
                "release_date": "1994-10-18",
            },
            content_type="application/json",
        ).json()
        cls.jesse_james = cls.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Jesse James",
                "album": cls.the_diary["id"],
                "track_number": 4,
                "length": 253,
                "path": "/scarface/the-diary/04_jesse_james.flac",
            },
            content_type="application/json",
        ).json()
        cls.greatest_hits = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "Greatest Hits",
                "release_date": "2002-10-22",
            },
            content_type="application/json",
        ).json()

    def test_update_song_status_code(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.jesse_james["id"]}),
            {
                "title": "Jesse James",
                "album": self.greatest_hits["id"],
                "disc": 1,
                "track_number": 16,
                "length": 253,
                "path": "/scarface/greatest-hits/16_jesse_james.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

    def test_update_song_json_response(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.jesse_james["id"]}),
            {
                "title": "Jesse James",
                "album": self.greatest_hits["id"],
                "disc": 1,
                "track_number": 16,
                "length": 253,
                "path": "/scarface/greatest-hits/16_jesse_james.flac",
            },
            content_type="application/json",
        ).json()

        self.assertEqual(response["id"], self.jesse_james["id"])
        self.assertEqual(response["title"], "Jesse James")
        self.assertEqual(len(response["artists"]), 0)
        self.assertEqual(len(response["producers"]), 0)
        self.assertEqual(response["album"]["title"], "Greatest Hits")
        self.assertEqual(response["disc"], 1)
        self.assertEqual(response["track_number"], 16)
        self.assertEqual(response["length"], 253)
        self.assertEqual(response["path"], "/scarface/greatest-hits/16_jesse_james.flac")
        self.assertEqual(response["play_count"], 0)
        self.assertTrue(response["url"].endswith(f"/api/v1/songs/{self.jesse_james["id"]}"))

    def test_update_song_with_extraneous_whitespace(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.jesse_james["id"]}),
            {
                "title": "          Jesse James           ",
                "album": self.greatest_hits["id"],
                "disc": 1,
                "track_number": 16,
                "length": 253,
                "path": "/scarface/greatest-hits/16_jesse_james.flac              ",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Jesse James")
        self.assertEqual(response.json()["path"], "/scarface/greatest-hits/16_jesse_james.flac")

    def test_update_song_with_extraneous_fields(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.jesse_james["id"]}),
            {
                "title": "Jesse James",
                "album": self.greatest_hits["id"],
                "disc": 1,
                "track_number": 16,
                "length": 253,
                "path": "/scarface/greatest-hits/16_jesse_james.flac",
                "engineer": "Mike Dean",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Jesse James")
        self.assertFalse("engineer" in response.json().keys())

    def test_update_unknown_song(self):
        song_id = self.jesse_james["id"] + 100
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": song_id}),
            {
                "title": "Jesse James",
                "album": self.greatest_hits["id"],
                "disc": 1,
                "track_number": 16,
                "length": 253,
                "path": "/scarface/greatest-hits/16_jesse_james.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Song with id = {song_id} does not exist."
        )

    def test_update_song_with_unknown_album(self):
        album_id = self.greatest_hits["id"] + 100
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.jesse_james["id"]}),
            {
                "title": "Jesse James",
                "album": album_id,
                "disc": 1,
                "track_number": 16,
                "length": 253,
                "path": "/scarface/greatest-hits/16_jesse_james.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Album with id = {album_id} does not exist."
        )

    def test_update_song_with_missing_required_fields(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.jesse_james["id"]}),
            {
                "album": self.greatest_hits["id"],
                "disc": 1,
                "track_number": 16,
                "path": "/scarface/greatest-hits/16_jesse_james.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_update_song_with_invalid_values(self):
        response = self.client.put(
            reverse("api-1.0:update_song", kwargs={"id": self.jesse_james["id"]}),
            {
                "title": "Jesse James",
                "album": "Greatest Hits",
                "disc": 1,
                "track_number": 16,
                "length": 253,
                "path": "/scarface/greatest-hits/16_jesse_james.flac",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)


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
                "title": "Sippin' On Some Syrup",
                "album": cls.when_the_smoke_clears["id"],
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

    def test_deleted_song_does_not_exist(self):
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


class CreateSongArtistTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.goodie_mob = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Goodie Mob"},
            content_type="application/json",
        ).json()
        cls.big_boi = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Big Boi"},
            content_type="application/json",
        ).json()
        cls.big_gipp = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Big Gipp"},
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
        cls.dirty_south = cls.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Dirty South",
                "album": cls.soul_food["id"],
                "track_number": 4,
                "length": 214,
                "path": "/goodie-mob/soul-food/04_dirty_south.flac",
            },
            content_type="application/json",
        ).json()

    def test_create_valid_song_artist_status_code(self):
        response = self.client.post(
            reverse("api-1.0:create_song_artist", kwargs={"id": self.dirty_south["id"]}),
            {"artist": self.goodie_mob["id"]},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_song_artist_json_response(self):
        response = self.client.post(
            reverse("api-1.0:create_song_artist", kwargs={"id": self.dirty_south["id"]}),
            {"artist": self.goodie_mob["id"]},
            content_type="application/json",
        ).json()

        self.assertEqual(response["song"]["title"], "Dirty South")
        self.assertEqual(response["artist"]["name"], "Goodie Mob")
        self.assertFalse(response["group"])

    def test_create_valid_group_artist_status_code(self):
        response = self.client.post(
            reverse("api-1.0:create_song_artist", kwargs={"id": self.dirty_south["id"]}),
            {
                "artist": self.big_gipp["id"],
                "group": True,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_group_artist_json_response(self):
        response = self.client.post(
            reverse("api-1.0:create_song_artist", kwargs={"id": self.dirty_south["id"]}),
            {
                "artist": self.big_gipp["id"],
                "group": True,
            },
            content_type="application/json",
        ).json()

        self.assertEqual(response["song"]["title"], "Dirty South")
        self.assertEqual(response["artist"]["name"], "Big Gipp")
        self.assertTrue(response["group"])

    def test_create_song_artist_with_extraneous_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_song_artist", kwargs={"id": self.dirty_south["id"]}),
            {
                "artist": self.goodie_mob["id"],
                "order": 1,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["artist"]["name"], "Goodie Mob")
        self.assertFalse("order" in response.json().keys())

    def test_create_song_artist_with_unknown_song(self):
        song_id = self.dirty_south["id"] + 100
        response = self.client.post(
            reverse("api-1.0:create_song_artist", kwargs={"id": song_id}),
            {"artist": self.goodie_mob["id"]},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Song with id = {song_id} does not exist."
        )

    def test_create_song_artist_with_unknown_artist(self):
        artist_id = self.goodie_mob["id"] + 100
        response = self.client.post(
            reverse("api-1.0:create_song_artist", kwargs={"id": self.dirty_south["id"]}),
            {"artist": artist_id},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Artist with id = {artist_id} does not exist."
        )

    def test_create_duplicate_song_artist(self):
        self.client.post(
            reverse("api-1.0:create_song_artist", kwargs={"id": self.dirty_south["id"]}),
            {"artist": self.goodie_mob["id"]},
            content_type="application/json",
        )

        response = self.client.post(
            reverse("api-1.0:create_song_artist", kwargs={"id": self.dirty_south["id"]}),
            {
                "artist": self.goodie_mob["id"],
                "group": True,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        message = (f"Artist with id = {self.goodie_mob["id"]} is already credited "
                   f"as an artist for song with id = {self.dirty_south["id"]}.")
        self.assertEqual(response.json()["error"], message)

    def test_create_song_artist_with_missing_required_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_song_artist", kwargs={"id": self.dirty_south["id"]}),
            {},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_create_song_artist_with_invalid_values(self):
        response = self.client.post(
            reverse("api-1.0:create_song_artist", kwargs={"id": self.dirty_south["id"]}),
            {"artist": "Goodie Mob"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)


class RetrieveAllSongArtistsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.master_p = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Master P"},
            content_type="application/json",
        ).json()
        cls.tru = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Tru"},
            content_type="application/json",
        ).json()
        cls.ghetto_d = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "Ghetto D",
                "release_date": "1997-09-02",
            },
            content_type="application/json",
        ).json()
        cls.make_em_say_uhh = cls.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Make 'Em Say Uhh!",
                "album": cls.ghetto_d["id"],
                "track_number": 12,
                "length": 306,
                "path": "/master-p/ghetto-d/12_make_em_say_uhh.flac",
            },
            content_type="application/json",
        ).json()
        cls.client.post(
            reverse("api-1.0:create_song_artist", kwargs={"id": cls.make_em_say_uhh["id"]}),
            {"artist": cls.master_p["id"]},
            content_type="application/json",
        )
        cls.client.post(
            reverse("api-1.0:create_song_artist", kwargs={"id": cls.make_em_say_uhh["id"]}),
            {
                "artist": cls.tru["id"],
                "group": True,
            },
            content_type="application/json",
        )

    def test_retrieve_song_artists_status_code(self):
        response = self.client.get(
            reverse(
                "api-1.0:retrieve_song_artists",
                kwargs={"id": self.make_em_say_uhh["id"]},
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_retrieve_song_artists_json_response(self):
        response = self.client.get(
            reverse(
                "api-1.0:retrieve_song_artists",
                kwargs={"id": self.make_em_say_uhh["id"]},
            )
        ).json()

        self.assertEqual(response["id"], self.make_em_say_uhh["id"])
        self.assertEqual(response["title"], "Make 'Em Say Uhh!")
        self.assertEqual(response["artists"][0]["id"], self.master_p["id"])
        self.assertEqual(response["artists"][0]["name"], "Master P")
        self.assertFalse(response["artists"][0]["group"])
        self.assertTrue(response["artists"][0]["url"].endswith(f"/api/v1/artists/{self.master_p["id"]}"))
        self.assertEqual(response["artists"][1]["id"], self.tru["id"])
        self.assertEqual(response["artists"][1]["name"], "Tru")
        self.assertTrue(response["artists"][1]["group"])
        self.assertTrue(response["artists"][1]["url"].endswith(f"/api/v1/artists/{self.tru["id"]}"))
        self.assertTrue(response["url"].endswith(f"/api/v1/songs/{self.make_em_say_uhh["id"]}"))

    def test_retrieve_song_artists_song_has_no_artists(self):
        i_miss_my_homies = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "I Miss My Homies",
                "album": self.ghetto_d["id"],
                "track_number": 3,
                "length": 325,
                "path": "/master-p/ghetto-d/03_i_miss_my_homies.flac",
            },
            content_type="application/json",
        ).json()
        response = self.client.get(
            reverse(
                "api-1.0:retrieve_song_artists",
                kwargs={"id": i_miss_my_homies["id"]},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["artists"]), 0)

    def test_retrieve_song_artists_unknown_song(self):
        song_id = self.make_em_say_uhh["id"] + 100
        response = self.client.get(
            reverse("api-1.0:retrieve_song_artists", kwargs={"id": song_id})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Song with id = {song_id} does not exist."
        )


class DeleteSongArtistTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.juvenile = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Juvenile"},
            content_type="application/json",
        ).json()
        cls.four_hundred_degreez = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "400 Degreez",
                "release_date": "1998-11-03",
            },
            content_type="application/json",
        ).json()
        cls.back_that_azz_up = cls.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Back That Azz Up",
                "album": cls.four_hundred_degreez["id"],
                "track_number": 13,
                "length": 265,
                "path": "/juvenile/400-degreez/13_back_that_azz_up.flac",
            },
            content_type="application/json",
        ).json()
        cls.client.post(
            reverse(
                "api-1.0:create_song_artist",
                kwargs={"id": cls.back_that_azz_up["id"]},
            ),
            {"artist": cls.juvenile["id"]},
            content_type="application/json",
        )

    def test_delete_song_artist_status_code(self):
        response = self.client.delete(
            reverse(
                "api-1.0:delete_song_artist",
                kwargs={
                    "song_id": self.back_that_azz_up["id"],
                    "artist_id": self.juvenile["id"],
                },
            )
        )

        self.assertEqual(response.status_code, 204)

    def test_delete_song_artist_json_response(self):
        response = self.client.delete(
            reverse(
                "api-1.0:delete_song_artist",
                kwargs={
                    "song_id": self.back_that_azz_up["id"],
                    "artist_id": self.juvenile["id"],
                },
            )
        )

        self.assertFalse(response.content)

    def test_deleted_song_artist_is_not_linked_to_song(self):
        song_artists = self.client.get(
            reverse(
                "api-1.0:retrieve_song_artists",
                kwargs={"id": self.back_that_azz_up["id"]},
            )
        ).json()
        self.assertEqual(len(song_artists["artists"]), 1)
        self.assertEqual(song_artists["artists"][0]["name"], "Juvenile")

        self.client.delete(
            reverse(
                "api-1.0:delete_song_artist",
                kwargs={
                    "song_id": self.back_that_azz_up["id"],
                    "artist_id": self.juvenile["id"],
                },
            )
        )

        song_artists = self.client.get(
            reverse(
                "api-1.0:retrieve_song_artists",
                kwargs={"id": self.back_that_azz_up["id"]},
            )
        ).json()
        self.assertEqual(len(song_artists["artists"]), 0)

    def test_delete_song_artist_with_unknown_song(self):
        song_id = self.back_that_azz_up["id"] + 100
        response = self.client.delete(
            reverse(
                "api-1.0:delete_song_artist",
                kwargs={
                    "song_id": song_id,
                    "artist_id": self.juvenile["id"],
                },
            )
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Song with id = {song_id} does not exist."
        )

    def test_delete_song_artist_with_unknown_artist(self):
        artist_id = self.juvenile["id"] + 100
        response = self.client.delete(
            reverse(
                "api-1.0:delete_song_artist",
                kwargs={
                    "song_id": self.back_that_azz_up["id"],
                    "artist_id": artist_id,
                },
            )
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Artist with id = {artist_id} does not exist."
        )


class CreateSongProducerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.ti = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "T.I."},
            content_type="application/json",
        ).json()
        cls.dj_toomp = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "DJ Toomp"},
            content_type="application/json",
        ).json()
        cls.trap_muzik = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "Trap Muzik",
                "release_date": "2003-08-19",
            },
            content_type="application/json",
        ).json()
        cls.be_easy = cls.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Be Easy",
                "album": cls.trap_muzik["id"],
                "track_number": 3,
                "length": 198,
                "path": "/ti/trap-muzik/03_be_easy.flac",
            },
            content_type="application/json",
        ).json()

    def test_create_valid_song_producer_status_code(self):
        response = self.client.post(
            reverse("api-1.0:create_song_producer", kwargs={"id": self.be_easy["id"]}),
            {
                "producer": self.dj_toomp["id"],
                "role": "Producer",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_valid_song_producer_json_response(self):
        response = self.client.post(
            reverse("api-1.0:create_song_producer", kwargs={"id": self.be_easy["id"]}),
            {
                "producer": self.dj_toomp["id"],
                "role": "Producer",
            },
            content_type="application/json",
        ).json()

        self.assertEqual(response["song"]["title"], "Be Easy")
        self.assertEqual(response["producer"]["name"], "DJ Toomp")
        self.assertEqual(response["role"], "Producer")

    def test_create_song_producer_with_extraneous_whitespace(self):
        response = self.client.post(
            reverse("api-1.0:create_song_producer", kwargs={"id": self.be_easy["id"]}),
            {
                "producer": self.dj_toomp["id"],
                "role": "           Producer",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["role"], "Producer")

    def test_create_song_producer_with_extraneous_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_song_producer", kwargs={"id": self.be_easy["id"]}),
            {
                "producer": self.dj_toomp["id"],
                "role": "Producer",
                "order": 1,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["producer"]["name"], "DJ Toomp")
        self.assertFalse("order" in response.json().keys())

    def test_create_song_producer_with_unknown_song(self):
        song_id = self.be_easy["id"] + 100
        response = self.client.post(
            reverse("api-1.0:create_song_producer", kwargs={"id": song_id}),
            {
                "producer": self.dj_toomp["id"],
                "role": "Producer",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Song with id = {song_id} does not exist."
        )

    def test_create_song_producer_with_unknown_artist(self):
        artist_id = self.dj_toomp["id"] + 100
        response = self.client.post(
            reverse("api-1.0:create_song_producer", kwargs={"id": self.be_easy["id"]}),
            {
                "producer": artist_id,
                "role": "Producer",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Artist with id = {artist_id} does not exist."
        )

    def test_create_duplicate_producer(self):
        self.client.post(
            reverse("api-1.0:create_song_producer", kwargs={"id": self.be_easy["id"]}),
            {
                "producer": self.dj_toomp["id"],
                "role": "Producer",
            },
            content_type="application/json",
        )

        response = self.client.post(
            reverse("api-1.0:create_song_producer", kwargs={"id": self.be_easy["id"]}),
            {
                "producer": self.dj_toomp["id"],
                "role": "Co-Producer",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        message = (f"Artist with id = {self.dj_toomp["id"]} is already credited "
                   f"as a producer for song with id = {self.be_easy["id"]}.")
        self.assertEqual(response.json()["error"], message)

    def test_create_song_producer_with_missing_required_fields(self):
        response = self.client.post(
            reverse("api-1.0:create_song_producer", kwargs={"id": self.be_easy["id"]}),
            {"producer": self.dj_toomp["id"]},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_create_song_producer_with_invalid_values(self):
        response = self.client.post(
            reverse("api-1.0:create_song_producer", kwargs={"id": self.be_easy["id"]}),
            {
                "producer": "DJ Toomp",
                "role": "Producer",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)


class RetrieveAllSongProducersTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.kanye_west = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Kanye West"},
            content_type="application/json",
        ).json()
        cls.ludacris = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Ludacris"},
            content_type="application/json",
        ).json()
        cls.chicken_n_beer = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "Chicken-N-Beer",
                "release_date": "2003-10-07",
            },
            content_type="application/json",
        ).json()
        cls.stand_up = cls.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Stand Up",
                "album": cls.chicken_n_beer["id"],
                "track_number": 3,
                "length": 213,
                "path": "/ludacris/chicken-n-beer/03_stand_up.flac",
            },
            content_type="application/json",
        ).json()
        cls.client.post(
            reverse("api-1.0:create_song_producer", kwargs={"id": cls.stand_up["id"]}),
            {
                "producer": cls.kanye_west["id"],
                "role": "Producer",
            },
            content_type="application/json",
        )
        cls.client.post(
            reverse("api-1.0:create_song_producer", kwargs={"id": cls.stand_up["id"]}),
            {
                "producer": cls.ludacris["id"],
                "role": "Co-Producer",
            },
            content_type="application/json",
        )

    def test_retrieve_song_producers_status_code(self):
        response = self.client.get(
            reverse(
                "api-1.0:retrieve_song_producers",
                kwargs={"id": self.stand_up["id"]},
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_retrieve_song_producers_json_response(self):
        response = self.client.get(
            reverse(
                "api-1.0:retrieve_song_producers",
                kwargs={"id": self.stand_up["id"]},
            )
        ).json()

        self.assertEqual(response["id"], self.stand_up["id"])
        self.assertEqual(response["title"], "Stand Up")
        self.assertEqual(response["producers"][0]["id"], self.kanye_west["id"])
        self.assertEqual(response["producers"][0]["name"], "Kanye West")
        self.assertEqual(response["producers"][0]["role"], "Producer")
        self.assertTrue(response["producers"][0]["url"].endswith(f"/api/v1/artists/{self.kanye_west["id"]}"))
        self.assertEqual(response["producers"][1]["id"], self.ludacris["id"])
        self.assertEqual(response["producers"][1]["name"], "Ludacris")
        self.assertEqual(response["producers"][1]["role"], "Co-Producer")
        self.assertTrue(response["producers"][1]["url"].endswith(f"/api/v1/artists/{self.ludacris["id"]}"))
        self.assertTrue(response["url"].endswith(f"/api/v1/songs/{self.stand_up["id"]}"))

    def test_retrieve_song_producers_song_has_no_producers(self):
        we_got = self.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "We Got",
                "album": self.chicken_n_beer["id"],
                "track_number": 16,
                "length": 261,
                "path": "/ludacris/chicken-n-beer/16_we_got.flac",
            },
            content_type="application/json",
        ).json()
        response = self.client.get(
            reverse(
                "api-1.0:retrieve_song_producers",
                kwargs={"id": we_got["id"]},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["producers"]), 0)

    def test_retrieve_song_producers_unknown_song(self):
        song_id = self.stand_up["id"] + 100
        response = self.client.get(
            reverse("api-1.0:retrieve_song_producers", kwargs={"id": song_id})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Song with id = {song_id} does not exist."
        )


class DeleteSongProducerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.mannie_fresh = cls.client.post(
            reverse("api-1.0:create_artist"),
            {"name": "Mannie Fresh"},
            content_type="application/json",
        ).json()
        cls.tha_carter = cls.client.post(
            reverse("api-1.0:create_album"),
            {
                "title": "Tha Carter",
                "release_date": "2004-06-29",
            },
            content_type="application/json",
        ).json()
        cls.go_dj = cls.client.post(
            reverse("api-1.0:create_song"),
            {
                "title": "Go DJ",
                "album": cls.tha_carter["id"],
                "track_number": 2,
                "length": 282,
                "path": "/lil-wayne/tha-carter/02_go_dj.flac",
            },
            content_type="application/json",
        ).json()
        cls.client.post(
            reverse(
                "api-1.0:create_song_producer",
                kwargs={"id": cls.go_dj["id"]},
            ),
            {
                "producer": cls.mannie_fresh["id"],
                "role": "Producer",
            },
            content_type="application/json",
        )

    def test_delete_song_producer_status_code(self):
        response = self.client.delete(
            reverse(
                "api-1.0:delete_song_producer",
                kwargs={
                    "song_id": self.go_dj["id"],
                    "producer_id": self.mannie_fresh["id"],
                },
            )
        )

        self.assertEqual(response.status_code, 204)

    def test_delete_song_producer_json_response(self):
        response = self.client.delete(
            reverse(
                "api-1.0:delete_song_producer",
                kwargs={
                    "song_id": self.go_dj["id"],
                    "producer_id": self.mannie_fresh["id"],
                },
            )
        )

        self.assertFalse(response.content)

    def test_deleted_song_producer_is_not_linked_to_song(self):
        song_producers = self.client.get(
            reverse(
                "api-1.0:retrieve_song_producers",
                kwargs={"id": self.go_dj["id"]},
            )
        ).json()
        self.assertEqual(len(song_producers["producers"]), 1)
        self.assertEqual(song_producers["producers"][0]["name"], "Mannie Fresh")

        self.client.delete(
            reverse(
                "api-1.0:delete_song_producer",
                kwargs={
                    "song_id": self.go_dj["id"],
                    "producer_id": self.mannie_fresh["id"],
                },
            )
        )

        song_producers = self.client.get(
            reverse(
                "api-1.0:retrieve_song_producers",
                kwargs={"id": self.go_dj["id"]},
            )
        ).json()
        self.assertEqual(len(song_producers["producers"]), 0)

    def test_delete_song_producer_with_unknown_song(self):
        song_id = self.go_dj["id"] + 100
        response = self.client.delete(
            reverse(
                "api-1.0:delete_song_producer",
                kwargs={
                    "song_id": song_id,
                    "producer_id": self.mannie_fresh["id"],
                },
            )
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Song with id = {song_id} does not exist."
        )

    def test_delete_song_producer_with_unknown_artist(self):
        producer_id = self.mannie_fresh["id"] + 100
        response = self.client.delete(
            reverse(
                "api-1.0:delete_song_producer",
                kwargs={
                    "song_id": self.go_dj["id"],
                    "producer_id": producer_id,
                },
            )
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"], f"Artist with id = {producer_id} does not exist."
        )
