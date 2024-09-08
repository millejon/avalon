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

    def test_album_creation_album_type_album_by_default(self):
        self.assertEqual(self.the_chronic.album_type, "album")

    def test_artists_related_name_is_album_artists(self):
        related_name = self.the_chronic._meta.get_field("artists")._related_name

        self.assertEqual(related_name, "album_artists")

    def test_album_title_max_length_is_600(self):
        max_length = self.the_chronic._meta.get_field("title").max_length

        self.assertEqual(max_length, 600)

    def test_album_type_max_length_is_10(self):
        max_length = self.the_chronic._meta.get_field("album_type").max_length

        self.assertEqual(max_length, 10)

    def test_album_type_has_three_choices(self):
        types = [("album", "album"), ("multidisc", "multidisc"), ("single", "single")]
        type_choices = self.the_chronic._meta.get_field("album_type").choices

        self.assertEqual(types, type_choices)

    def test_str_method_returns_album_title(self):
        self.assertEqual(str(self.the_chronic), "The Chronic")

    def test_get_url_method_returns_album_api_url(self):
        self.assertEqual(
            self.the_chronic.get_url(), f"/api/v1/albums/{self.the_chronic.id}"
        )

    def test_get_artists_url_method_returns_album_artists_api_url(self):
        self.assertEqual(
            self.the_chronic.get_artists_url(),
            f"/api/v1/albums/{self.the_chronic.id}/artists",
        )

    def test_get_songs_url_method_returns_album_songs_api_url(self):
        self.assertEqual(
            self.the_chronic.get_songs_url(),
            f"/api/v1/albums/{self.the_chronic.id}/songs",
        )

    def test_get_discs_url_method_returns_album_discs_api_url(self):
        self.assertEqual(
            self.the_chronic.get_discs_url(),
            f"/api/v1/albums/{self.the_chronic.id}/discs",
        )

    def test_duplicate_album_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Album.objects.create(
                title="The Chronic",
                release_date=datetime.date(1992, 12, 15),
                album_type="multidisc",
            )

    def test_duplicate_album_creation_case_insensitive_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Album.objects.create(
                title="the chronic",
                release_date=datetime.date(1992, 12, 15),
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
        cls.the_alchemist = models.Artist.objects.create(name="The Alchemist")
        cls.prodigy = models.Artist.objects.create(name="Prodigy")
        cls.albert_einstein = models.Album.objects.create(
            title="Albert Einstein",
            release_date=datetime.date(2013, 6, 11),
        )
        cls.album_artist_link = models.AlbumArtist.objects.create(
            album=cls.albert_einstein, artist=cls.prodigy
        )

    def test_album_artist_creation_successful(self):
        self.assertEqual(self.album_artist_link.album.title, "Albert Einstein")
        self.assertEqual(self.album_artist_link.artist.name, "Prodigy")

    def test_str_method_returns_album_title_artist_name(self):
        self.assertEqual(str(self.album_artist_link), "Albert Einstein - Prodigy")

    def test_duplicate_album_artist_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.AlbumArtist.objects.create(
                album=self.albert_einstein, artist=self.prodigy
            )

    def test_album_artists_ordered_by_albumartist_id(self):
        models.AlbumArtist.objects.create(
            album=self.albert_einstein, artist=self.the_alchemist
        )
        album_artists = [str(artist) for artist in models.AlbumArtist.objects.all()]

        self.assertEqual(
            album_artists,
            ["Albert Einstein - Prodigy", "Albert Einstein - The Alchemist"],
        )


class DiscModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.life_after_death = models.Album.objects.create(
            title="Life After Death",
            release_date=datetime.date(1997, 3, 25),
            album_type="multidisc",
        )
        cls.disc_two = models.Disc.objects.create(
            album=cls.life_after_death, number=2, title="Disc Two"
        )

    def test_disc_creation_successful(self):
        self.assertEqual(self.disc_two.album.title, "Life After Death")
        self.assertEqual(self.disc_two.number, 2)
        self.assertEqual(self.disc_two.title, "Disc Two")

    def test_disc_title_max_length_is_100(self):
        max_length = self.disc_two._meta.get_field("title").max_length

        self.assertEqual(max_length, 100)

    def test_str_method_returns_album_title_disc_title(self):
        self.assertEqual(str(self.disc_two), "Life After Death (Disc Two)")

    def test_get_url_method_returns_disc_api_url(self):
        self.assertEqual(self.disc_two.get_url(), f"/api/v1/discs/{self.disc_two.id}")

    def test_duplicate_disc_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Disc.objects.create(
                album=self.life_after_death, number=2, title="Disc Two"
            )

    def test_duplicate_disc_creation_case_insensitive_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Disc.objects.create(
                album=self.life_after_death, number=2, title="DISC TWO"
            )

    def test_disc_creation_duplicate_number_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Disc.objects.create(
                album=self.life_after_death, number=2, title="Disc 2"
            )

    def test_disc_creation_duplicate_title_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Disc.objects.create(
                album=self.life_after_death, number=1, title="Disc Two"
            )

    def test_disc_creation_number_less_than_one_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Disc.objects.create(
                album=self.life_after_death, number=0, title="Disc Zero"
            )

    def test_discs_ordered_by_number(self):
        models.Disc.objects.create(
            album=self.life_after_death, number=1, title="Disc One"
        )
        discs = [str(disc) for disc in models.Disc.objects.all()]

        self.assertEqual(
            discs, ["Life After Death (Disc One)", "Life After Death (Disc Two)"]
        )


class SongModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.me_against_the_world = models.Album.objects.create(
            title="Me Against The World",
            release_date=datetime.date(1995, 3, 14),
        )
        cls.all_eyez_on_me = models.Album.objects.create(
            title="All Eyez On Me",
            release_date=datetime.date(1996, 2, 13),
            album_type="multidisc",
        )
        cls.temptations = models.Song.objects.create(
            title="Temptations",
            album=cls.me_against_the_world,
            track_number=5,
            length=301,
            path="/2pac/me-against-the-world/05_temptations.flac",
        )

    def test_song_creation_successful(self):
        self.assertEqual(self.temptations.title, "Temptations")
        self.assertEqual(self.temptations.album.title, "Me Against The World")
        self.assertEqual(self.temptations.track_number, 5)
        self.assertEqual(self.temptations.length, 301)
        self.assertEqual(
            self.temptations.path, "/2pac/me-against-the-world/05_temptations.flac"
        )

    def test_song_creation_disc_one_by_default(self):
        self.assertEqual(self.temptations.disc, 1)

    def test_song_creation_play_count_zero_by_default(self):
        self.assertEqual(self.temptations.play_count, 0)

    def test_song_title_max_length_is_600(self):
        max_length = self.temptations._meta.get_field("title").max_length

        self.assertEqual(max_length, 600)

    def test_artists_related_name_is_song_artists(self):
        related_name = self.temptations._meta.get_field("artists")._related_name

        self.assertEqual(related_name, "song_artists")

    def test_producers_related_name_is_song_artists(self):
        related_name = self.temptations._meta.get_field("producers")._related_name

        self.assertEqual(related_name, "song_producers")

    def test_song_path_max_length_is_1000(self):
        max_length = self.temptations._meta.get_field("path").max_length

        self.assertEqual(max_length, 1000)

    def test_song_path_unique_constraint_is_true(self):
        unique_constraint = self.temptations._meta.get_field("path").unique

        self.assertTrue(unique_constraint)

    def test_str_method_returns_track_number_song_title_album_title(self):
        self.assertEqual(str(self.temptations), "5. Temptations [Me Against The World]")

    def test_get_url_method_returns_song_api_url(self):
        self.assertEqual(
            self.temptations.get_url(), f"/api/v1/songs/{self.temptations.id}"
        )

    def test_get_artists_url_method_returns_song_artists_api_url(self):
        self.assertEqual(
            self.temptations.get_artists_url(),
            f"/api/v1/songs/{self.temptations.id}/artists",
        )

    def test_get_producers_url_method_returns_song_producers_api_url(self):
        self.assertEqual(
            self.temptations.get_producers_url(),
            f"/api/v1/songs/{self.temptations.id}/producers",
        )

    def test_duplicate_song_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="Temptations",
                album=self.me_against_the_world,
                track_number=5,
                length=303,
                path="/2pac/me-against-the-world/05_temptations.flac",
            )

    def test_song_creation_duplicate_track_number_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="So Many Tears",
                album=self.me_against_the_world,
                track_number=5,
                length=239,
                path="/2pac/me-against-the-world/05_so_many_tears.flac",
            )

    def test_duplicate_song_creation_case_insensitive_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="TEMPTATIONS",
                album=self.me_against_the_world,
                track_number=5,
                length=303,
                path="/2Pac/Me-Against-The-World/05_Temptations.flac",
            )

    def test_song_creation_invalid_disc_number_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="Heavy In The Game",
                album=self.me_against_the_world,
                disc=0,
                track_number=7,
                length=265,
                path="/2pac/me-against-the-world/07_heavy_in_the_game.flac",
            )

    def test_song_creation_invalid_track_number_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="Lost Souls",
                album=self.me_against_the_world,
                track_number=0,
                length=283,
                path="/2pac/me-against-the-world/00_lost_souls.flac",
            )

    def test_songs_ordered_by_play_count_release_date_disc_number_track_number(self):
        models.Song.objects.create(
            title="If I Die 2Nite",
            album=self.me_against_the_world,
            track_number=2,
            length=242,
            path="/2pac/me-against-the-world/02_if_i_die_2nite.flac",
            play_count=2,
        )
        models.Song.objects.create(
            title="Death Around The Corner",
            album=self.me_against_the_world,
            track_number=14,
            length=247,
            path="/2pac/me-against-the-world/14_death_around_the_corner.flac",
            play_count=3,
        )
        models.Song.objects.create(
            title="Holla At Me",
            album=self.all_eyez_on_me,
            disc=2,
            track_number=3,
            length=295,
            path="/2pac/all-eyez-on-me/book-2/03_holla_at_me.flac",
        )
        models.Song.objects.create(
            title="California Love (Remix)",
            album=self.all_eyez_on_me,
            disc=1,
            track_number=12,
            length=385,
            path="/2pac/all-eyez-on-me/book-1/12_california_love_remix.flac",
        )
        models.Song.objects.create(
            title="Ambitionz Az A Ridah",
            album=self.all_eyez_on_me,
            disc=1,
            track_number=1,
            length=279,
            path="/2pac/all-eyez-on-me/book-1/01_ambitionz_az_a_ridah.flac",
        )
        songs = [str(song) for song in models.Song.objects.all()]
        expected_song_order = [
            "14. Death Around The Corner [Me Against The World]",
            "2. If I Die 2Nite [Me Against The World]",
            "1. Ambitionz Az A Ridah [All Eyez On Me]",
            "12. California Love (Remix) [All Eyez On Me]",
            "3. Holla At Me [All Eyez On Me]",
            "5. Temptations [Me Against The World]",
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
                song=self.smooth, artist=self.tha_dogg_pound, group=True
            )

    def test_song_artists_ordered_by_songartist_id(self):
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
        cls.dj_clark_kent = models.Artist.objects.create(name="DJ Clark Kent")
        cls.damon_dash = models.Artist.objects.create(name="Damon Dash")
        cls.reasonable_doubt = models.Album.objects.create(
            title="Reasonable Doubt",
            release_date=datetime.date(1996, 6, 25),
        )
        cls.brooklyns_finest = models.Song.objects.create(
            title="Brooklyn's Finest",
            album=cls.reasonable_doubt,
            track_number=3,
            length=276,
            path="/jay-z/reasonable-doubt/03_brooklyns_finest.flac",
        )
        cls.song_producer = models.SongProducer.objects.create(
            song=cls.brooklyns_finest,
            producer=cls.damon_dash,
            role="Co-Producer",
        )

    def test_song_producer_creation_successful(self):
        self.assertEqual(self.song_producer.song.title, "Brooklyn's Finest")
        self.assertEqual(self.song_producer.producer.name, "Damon Dash")
        self.assertEqual(self.song_producer.role, "Co-Producer")

    def test_song_producer_role_max_length_is_100(self):
        max_length = self.song_producer._meta.get_field("role").max_length

        self.assertEqual(max_length, 100)

    def test_str_method_returns_song_title_producer_name_producer_role(self):
        self.assertEqual(
            str(self.song_producer),
            "Brooklyn's Finest - Damon Dash [Co-Producer]",
        )

    def test_duplicate_song_producer_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.SongProducer.objects.create(
                song=self.brooklyns_finest,
                producer=self.damon_dash,
                role="Producer",
            )

    def test_song_producers_ordered_by_songproducer_id(self):
        models.SongProducer.objects.create(
            song=self.brooklyns_finest,
            producer=self.dj_clark_kent,
            role="Producer",
        )
        song_producers = [
            str(producer) for producer in models.SongProducer.objects.all()
        ]
        expected_song_producer_order = [
            "Brooklyn's Finest - Damon Dash [Co-Producer]",
            "Brooklyn's Finest - DJ Clark Kent [Producer]",
        ]

        self.assertEqual(song_producers, expected_song_producer_order)
