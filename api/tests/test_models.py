import datetime

from django.test import TestCase
from django.db import IntegrityError

from api import models


class ArtistModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.raekwon = models.Artist.objects.create(name="Raekwon")

    def test_artist_creation_successful(self):
        self.assertEqual(self.raekwon.name, "Raekwon")

    def test_artist_name_max_length_is_100(self):
        max_length = self.raekwon._meta.get_field("name").max_length

        self.assertEqual(max_length, 100)

    def test_artist_name_unique_constraint_is_true(self):
        unique_constraint = self.raekwon._meta.get_field("name").unique

        self.assertTrue(unique_constraint)

    def test_str_method_returns_artist_name(self):
        self.assertEqual(str(self.raekwon), "Raekwon")

    def test_get_url_method_returns_artist_api_url(self):
        self.assertEqual(self.raekwon.get_url(), f"/api/v1/artists/{self.raekwon.id}")

    def test_get_albums_url_method_returns_artist_albums_api_url(self):
        self.assertEqual(
            self.raekwon.get_albums_url(),
            f"/api/v1/artists/{self.raekwon.id}/albums",
        )

    def test_get_singles_url_method_returns_artist_singles_api_url(self):
        self.assertEqual(
            self.raekwon.get_singles_url(),
            f"/api/v1/artists/{self.raekwon.id}/singles",
        )

    def test_get_songs_url_method_returns_artist_songs_api_url(self):
        self.assertEqual(
            self.raekwon.get_songs_url(), f"/api/v1/artists/{self.raekwon.id}/songs"
        )

    def test_get_credits_url_method_returns_artist_production_credits_api_url(self):
        self.assertEqual(
            self.raekwon.get_credits_url(),
            f"/api/v1/artists/{self.raekwon.id}/produced",
        )

    def test_duplicate_artist_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Artist.objects.create(name="Raekwon")

    def test_duplicate_artist_creation_case_insensitive_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Artist.objects.create(name="RaeKwon")

    def test_artists_ordered_by_name(self):
        models.Artist.objects.create(name="Ghostface Killah")
        models.Artist.objects.create(name="RZA")
        artists = [str(artist) for artist in models.Artist.objects.all()]

        self.assertEqual(artists, ["Ghostface Killah", "Raekwon", "RZA"])


class AlbumModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.the_chronic = models.Album.objects.create(
            title="The Chronic",
            release_date=datetime.date(1992, 12, 15),
        )

    def test_album_creation_successful(self):
        self.assertEqual(self.the_chronic.title, "The Chronic")
        self.assertEqual(self.the_chronic.release_date, datetime.date(1992, 12, 15))

    def test_album_creation_single_false_by_default(self):
        self.assertFalse(self.the_chronic.single)

    def test_album_creation_multidisc_false_by_default(self):
        self.assertFalse(self.the_chronic.multidisc)

    def test_single_creation_successful(self):
        how_do_u_want_it = models.Album.objects.create(
            title="How Do U Want It",
            release_date=datetime.date(1996, 6, 4),
            single=True,
        )

        self.assertEqual(how_do_u_want_it.title, "How Do U Want It")
        self.assertEqual(how_do_u_want_it.release_date, datetime.date(1996, 6, 4))
        self.assertTrue(how_do_u_want_it.single)

    def test_multidisc_album_creation_successful(self):
        chronic_2000 = models.Album.objects.create(
            title="Chronic 2000: Still Smokin'",
            release_date=datetime.date(1999, 5, 4),
            multidisc=True,
        )

        self.assertEqual(chronic_2000.title, "Chronic 2000: Still Smokin'")
        self.assertEqual(chronic_2000.release_date, datetime.date(1999, 5, 4))
        self.assertTrue(chronic_2000.multidisc)

    def test_album_title_max_length_is_600(self):
        max_length = self.the_chronic._meta.get_field("title").max_length

        self.assertEqual(max_length, 600)

    def test_artists_related_name_is_album_artists(self):
        related_name = self.the_chronic._meta.get_field("artists")._related_name

        self.assertEqual(related_name, "album_artists")

    def test_str_method_returns_album_title(self):
        self.assertEqual(str(self.the_chronic), "The Chronic")

    def test_get_url_method_returns_album_api_url(self):
        self.assertEqual(
            self.the_chronic.get_url(), f"/api/v1/albums/{self.the_chronic.id}"
        )

    def test_get_songs_url_method_returns_album_songs_api_url(self):
        self.assertEqual(
            self.the_chronic.get_songs_url(),
            f"/api/v1/albums/{self.the_chronic.id}/songs",
        )

    def test_duplicate_album_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Album.objects.create(
                title="The Chronic",
                release_date=datetime.date(1992, 12, 15),
            )

    def test_duplicate_album_creation_case_insensitive_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Album.objects.create(
                title="the chronic",
                release_date=datetime.date(1992, 12, 15),
            )

    def test_multidisc_single_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Album.objects.create(
                title="Deep Cover",
                release_date=datetime.date(1992, 4, 9),
                single=True,
                multidisc=True,
            )

    def test_albums_ordered_by_artist_name_then_release_date(self):
        self.the_chronic.artists.create(name="Dr. Dre")
        snoop_dogg = models.Artist.objects.create(name="Snoop Dogg")
        tha_doggfather = models.Album.objects.create(
            title="Tha Doggfather",
            release_date=datetime.date(1996, 11, 12),
        )
        tha_doggfather.artists.add(snoop_dogg)
        doggystyle = models.Album.objects.create(
            title="Doggystyle",
            release_date=datetime.date(1993, 11, 23),
        )
        doggystyle.artists.add(snoop_dogg)
        albums = [str(album) for album in models.Album.objects.all()]

        self.assertEqual(albums, ["The Chronic", "Doggystyle", "Tha Doggfather"])


class AlbumArtistModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dj_quik = models.Artist.objects.create(name="DJ Quik")
        cls.kurupt = models.Artist.objects.create(name="Kurupt")
        cls.blaqkout = models.Album.objects.create(
            title="Blaqkout",
            release_date=datetime.date(2009, 6, 9),
        )
        cls.album_artist = models.AlbumArtist.objects.create(
            album=cls.blaqkout, artist=cls.kurupt
        )

    def test_album_artist_creation_successful(self):
        self.assertEqual(self.album_artist.album.title, "Blaqkout")
        self.assertEqual(self.album_artist.artist.name, "Kurupt")

    def test_str_method_returns_album_title_artist_name(self):
        self.assertEqual(str(self.album_artist), "Blaqkout - Kurupt")

    def test_duplicate_album_artist_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.AlbumArtist.objects.create(album=self.blaqkout, artist=self.kurupt)

    def test_album_artists_ordered_by_id(self):
        models.AlbumArtist.objects.create(album=self.blaqkout, artist=self.dj_quik)
        album_artists = [str(artist) for artist in models.AlbumArtist.objects.all()]

        self.assertEqual(album_artists, ["Blaqkout - Kurupt", "Blaqkout - DJ Quik"])


class DiscModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.all_eyez_on_me = models.Album.objects.create(
            title="All Eyez On Me",
            release_date=datetime.date(1996, 2, 13),
            multidisc=True,
        )
        cls.book2 = models.Disc.objects.create(
            album=cls.all_eyez_on_me,
            number=2,
            title="Book 2",
        )

    def test_disc_creation_successful(self):
        self.assertEqual(self.book2.album.title, "All Eyez On Me")
        self.assertEqual(self.book2.number, 2)
        self.assertEqual(self.book2.title, "Book 2")

    def test_disc_title_max_length(self):
        max_length = self.book2._meta.get_field("title").max_length

        self.assertEqual(max_length, 100)

    def test_str_method_returns_album_title_disc_title(self):
        self.assertEqual(str(self.book2), "All Eyez On Me (Book 2)")

    def test_get_url_method_returns_disc_api_url(self):
        self.assertEqual(self.book2.get_url(), f"/api/v1/discs/{self.book2.id}")

    def test_duplicate_disc_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Disc.objects.create(
                album=self.all_eyez_on_me,
                number=2,
                title="Book 2",
            )

    def test_disc_creation_with_duplicate_number_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Disc.objects.create(
                album=self.all_eyez_on_me,
                number=2,
                title="Book 1",
            )

    def test_disc_creation_with_duplicate_title_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Disc.objects.create(
                album=self.all_eyez_on_me,
                number=1,
                title="Book 2",
            )

    def test_duplicate_disc_creation_case_insensitive_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Disc.objects.create(
                album=self.all_eyez_on_me,
                number=2,
                title="BOOK 2",
            )

    def test_disc_creation_with_invalid_number_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Disc.objects.create(
                album=self.all_eyez_on_me,
                number=0,
                title="Book 0",
            )

    def test_discs_ordered_by_number(self):
        models.Disc.objects.create(album=self.all_eyez_on_me, number=1, title="Book 1")
        discs = [str(disc) for disc in models.Disc.objects.all()]

        self.assertEqual(discs, ["All Eyez On Me (Book 1)", "All Eyez On Me (Book 2)"])


class SongModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.the_don_killuminati = models.Album.objects.create(
            title="The Don Killuminati: The 7 Day Theory",
            release_date=datetime.date(1996, 11, 5),
        )
        cls.r_u_still_down = models.Album.objects.create(
            title="R U Still Down? (Remember Me)",
            release_date=datetime.date(1997, 11, 25),
            multidisc=True,
        )
        cls.toss_it_up = models.Song.objects.create(
            title="Toss It Up",
            album=cls.the_don_killuminati,
            track_number=3,
            length=306,
            path="/2pac/the-don-killuminati-the-7-day-theory/03_toss_it_up.flac",
        )

    def test_song_creation_successful(self):
        self.assertEqual(self.toss_it_up.title, "Toss It Up")
        self.assertEqual(
            self.toss_it_up.album.title, "The Don Killuminati: The 7 Day Theory"
        )
        self.assertEqual(self.toss_it_up.track_number, 3)
        self.assertEqual(self.toss_it_up.length, 306)
        self.assertEqual(
            self.toss_it_up.path,
            "/2pac/the-don-killuminati-the-7-day-theory/03_toss_it_up.flac",
        )

    def test_song_creation_disc_null_by_default(self):
        self.assertIsNone(self.toss_it_up.disc)

    def test_song_creation_play_count_zero_by_default(self):
        self.assertEqual(self.toss_it_up.play_count, 0)

    def test_song_title_max_length_is_600(self):
        max_length = self.toss_it_up._meta.get_field("title").max_length

        self.assertEqual(max_length, 600)

    def test_artists_related_name_is_song_artists(self):
        related_name = self.toss_it_up._meta.get_field("artists")._related_name

        self.assertEqual(related_name, "song_artists")

    def test_producers_related_name_is_song_artists(self):
        related_name = self.toss_it_up._meta.get_field("producers")._related_name

        self.assertEqual(related_name, "song_producers")

    def test_song_path_max_length_is_1000(self):
        max_length = self.toss_it_up._meta.get_field("path").max_length

        self.assertEqual(max_length, 1000)

    def test_song_path_unique_constraint_is_true(self):
        unique_constraint = self.toss_it_up._meta.get_field("path").unique

        self.assertTrue(unique_constraint)

    def test_str_method_returns_track_number_song_title_album_title(self):
        self.assertEqual(
            str(self.toss_it_up),
            "3. Toss It Up [The Don Killuminati: The 7 Day Theory]",
        )

    def test_get_url_method_returns_song_api_url(self):
        self.assertEqual(
            self.toss_it_up.get_url(), f"/api/v1/songs/{self.toss_it_up.id}"
        )

    def test_duplicate_song_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="Toss It Up",
                album=self.the_don_killuminati,
                track_number=3,
                length=306,
                path="/2pac/the-don-killuminati-the-7-day-theory/03_toss_it_up.flac",
            )

    def test_song_creation_with_duplicate_track_number_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="Hail Mary",
                album=self.the_don_killuminati,
                track_number=3,
                length=310,
                path="/2pac/the-don-killuminati-the-7-day-theory/03_hail_mary.flac",
            )

    def test_duplicate_song_creation_case_insensitive_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="Toss It Up",
                album=self.the_don_killuminati,
                track_number=4,
                length=306,
                path="/2Pac/The-Don-Killuminati-The-7-Day-Theory/03_Toss_It_Up.flac",
            )

    def test_song_creation_with_invalid_disc_number_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="Hellrazor",
                album=self.r_u_still_down,
                disc=0,
                track_number=4,
                length=255,
                path="/2pac/r-u-still-down-remember-me/disc-one/04_hellrazor.flac",
            )

    def test_song_creation_with_invalid_track_number_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="Lost Souls",
                album=self.the_don_killuminati,
                track_number=0,
                length=283,
                path="/2pac/the-don-killuminati-the-7-day-theory/00_lost_souls.flac",
            )

    def test_songs_ordered_by_play_count_release_date_disc_number_track_number(self):
        models.Song.objects.create(
            title="Life Of An Outlaw",
            album=self.the_don_killuminati,
            track_number=6,
            length=296,
            path="/2pac/the-don-killuminati-the-7-day-theory/06_life_of_an_outlaw.flac",
            play_count=2,
        )
        models.Song.objects.create(
            title="Me and My Girlfriend",
            album=self.the_don_killuminati,
            track_number=10,
            length=308,
            path="/2pac/the-don-killuminati-the-7-day-theory/10_me_and_my_girlfriend.flac",
            play_count=3,
        )
        models.Song.objects.create(
            title="Do For Love",
            album=self.r_u_still_down,
            disc=2,
            track_number=6,
            length=282,
            path="/2pac/r-u-still-down-remember-me/disc-two/06_do_for_love.flac",
        )
        models.Song.objects.create(
            title="I'm Gettin' Money",
            album=self.r_u_still_down,
            disc=1,
            track_number=9,
            length=212,
            path="/2pac/r-u-still-down-remember-me/disc-one/09_im_gettin_money.flac",
        )
        models.Song.objects.create(
            title="Open Fire",
            album=self.r_u_still_down,
            disc=1,
            track_number=2,
            length=172,
            path="/2pac/r-u-still-down-remember-me/disc-one/02_open_fire.flac",
        )
        songs = [str(song) for song in models.Song.objects.all()]
        expected_song_order = [
            "10. Me and My Girlfriend [The Don Killuminati: The 7 Day Theory]",
            "6. Life Of An Outlaw [The Don Killuminati: The 7 Day Theory]",
            "2. Open Fire [R U Still Down? (Remember Me)]",
            "9. I'm Gettin' Money [R U Still Down? (Remember Me)]",
            "6. Do For Love [R U Still Down? (Remember Me)]",
            "3. Toss It Up [The Don Killuminati: The 7 Day Theory]",
        ]

        self.assertEqual(songs, expected_song_order)


class SongArtistModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tha_dogg_pound = models.Artist.objects.create(name="Tha Dogg Pound")
        cls.kurupt = models.Artist.objects.create(name="Kurupt")
        cls.snoop_dogg = models.Artist.objects.create(name="Snoop Dogg")
        cls.val_young = models.Artist.objects.create(name="Val Young")
        cls.dogg_food = models.Album.objects.create(
            title="Dogg Food", release_date=datetime.date(1995, 10, 31)
        )
        cls.smooth = models.Song.objects.create(
            title="Smooth",
            album=cls.dogg_food,
            track_number=5,
            length=275,
            path="/tha-dogg-pound/dogg-food/05_smooth.flac",
        )
        cls.song_artist = models.SongArtist.objects.create(
            song=cls.smooth, artist=cls.tha_dogg_pound
        )

    def test_song_artist_creation_successful(self):
        self.assertEqual(self.song_artist.song.title, "Smooth")
        self.assertEqual(self.song_artist.artist.name, "Tha Dogg Pound")

    def test_song_artist_creation_group_false_by_default(self):
        self.assertFalse(self.song_artist.group)

    def test_group_member_song_artist_creation_successful(self):
        group_feature = models.SongArtist.objects.create(
            song=self.smooth, artist=self.kurupt, group=True
        )

        self.assertEqual(group_feature.song.title, "Smooth")
        self.assertEqual(group_feature.artist.name, "Kurupt")
        self.assertTrue(group_feature.group)

    def test_str_method_returns_song_title_artist_name(self):
        self.assertEqual(str(self.song_artist), "Smooth - Tha Dogg Pound")

    def test_duplicate_song_artist_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.SongArtist.objects.create(
                song=self.smooth, artist=self.tha_dogg_pound
            )

    def test_duplicate_song_artist_as_group_member_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.SongArtist.objects.create(
                song=self.smooth, artist=self.tha_dogg_pound, group=True
            )

    def test_song_artists_ordered_by_id(self):
        models.SongArtist.objects.create(song=self.smooth, artist=self.snoop_dogg)
        models.SongArtist.objects.create(
            song=self.smooth, artist=self.kurupt, group=True
        )
        models.SongArtist.objects.create(song=self.smooth, artist=self.val_young)
        song_artists = [str(artist) for artist in models.SongArtist.objects.all()]
        expected_song_artist_order = [
            "Smooth - Tha Dogg Pound",
            "Smooth - Snoop Dogg",
            "Smooth - Kurupt",
            "Smooth - Val Young",
        ]

        self.assertEqual(song_artists, expected_song_artist_order)


class SongProducerModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.binky_mack = models.Artist.objects.create(name="Binky Mack")
        cls.ice_cube = models.Artist.objects.create(name="Ice Cube")
        cls.bow_down = models.Album.objects.create(
            title="Bow Down",
            release_date=datetime.date(1996, 10, 22),
        )
        cls.all_the_critics_in_new_york = models.Song.objects.create(
            title="All The Critics In New York",
            album=cls.bow_down,
            track_number=4,
            length=335,
            path="/westside-connection/bow-down/04_all_the_critics_in_new_york.flac",
        )
        cls.song_producer = models.SongProducer.objects.create(
            song=cls.all_the_critics_in_new_york,
            producer=cls.ice_cube,
            role="Co-Producer",
        )

    def test_song_producer_creation_successful(self):
        self.assertEqual(self.song_producer.song.title, "All The Critics In New York")
        self.assertEqual(self.song_producer.producer.name, "Ice Cube")
        self.assertEqual(self.song_producer.role, "Co-Producer")

    def test_song_producer_role_max_length_is_100(self):
        max_length = self.song_producer._meta.get_field("role").max_length

        self.assertEqual(max_length, 100)

    def test_str_method_returns_song_title_producer_name_role(self):
        self.assertEqual(
            str(self.song_producer),
            "All The Critics In New York - Ice Cube [Co-Producer]",
        )

    def test_duplicate_song_producer_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.SongProducer.objects.create(
                song=self.all_the_critics_in_new_york,
                producer=self.ice_cube,
                role="Co-Producer",
            )

    def test_duplicate_song_producer_with_different_role_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.SongProducer.objects.create(
                song=self.all_the_critics_in_new_york,
                producer=self.ice_cube,
                role="Producer",
            )

    def test_song_producers_ordered_by_id(self):
        models.SongProducer.objects.create(
            song=self.all_the_critics_in_new_york,
            producer=self.binky_mack,
            role="Producer",
        )
        song_producers = [
            str(producer) for producer in models.SongProducer.objects.all()
        ]
        expected_song_producer_order = [
            "All The Critics In New York - Ice Cube [Co-Producer]",
            "All The Critics In New York - Binky Mack [Producer]",
        ]

        self.assertEqual(song_producers, expected_song_producer_order)
