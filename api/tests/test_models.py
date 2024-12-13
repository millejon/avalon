import datetime

from django.test import TestCase
from django.db import IntegrityError

from api import models


class ArtistModelTestCase(TestCase):
    def setUp(self):
        self.tupac = models.Artist.objects.create(name="2Pac", hometown="Oakland, CA")

    def test_artist_creation_successful_name(self):
        self.assertEqual(self.tupac.name, "2Pac")

    def test_artist_creation_successful_hometown(self):
        self.assertEqual(self.tupac.hometown, "Oakland, CA")

    def test_artist_creation_without_hometown_successful(self):
        snoop_dogg = models.Artist.objects.create(name="Snoop Dogg")

        self.assertEqual(snoop_dogg.hometown, "")

    def test_artist_name_max_length_is_100(self):
        max_length = self.tupac._meta.get_field("name").max_length

        self.assertEqual(max_length, 100)

    def test_artist_name_has_unique_constraint(self):
        unique_constraint = self.tupac._meta.get_field("name").unique

        self.assertTrue(unique_constraint)

    def test_artist_hometown_max_length_is_100(self):
        max_length = self.tupac._meta.get_field("hometown").max_length

        self.assertEqual(max_length, 100)

    def test_artist_hometown_can_be_blank(self):
        blank = self.tupac._meta.get_field("hometown").blank

        self.assertTrue(blank)

    def test_artist_str_method_returns_artist_name(self):
        self.assertEqual(str(self.tupac), "2Pac")

    def test_artist_get_url_method_returns_artist_api_url(self):
        self.assertEqual(self.tupac.get_url(), f"/api/artists/{self.tupac.id}")

    def test_artist_get_albums_url_method_returns_artist_albums_api_url(self):
        self.assertEqual(
            self.tupac.get_albums_url(), f"/api/artists/{self.tupac.id}/albums"
        )

    def test_artist_get_singles_url_method_returns_artist_singles_api_url(self):
        self.assertEqual(
            self.tupac.get_singles_url(), f"/api/artists/{self.tupac.id}/singles"
        )

    def test_artist_get_songs_url_method_returns_artist_songs_api_url(self):
        self.assertEqual(
            self.tupac.get_songs_url(), f"/api/artists/{self.tupac.id}/songs"
        )

    def test_artist_get_songs_produced_url_method_returns_artist_production_credits_api_url(
        self,
    ):
        self.assertEqual(
            self.tupac.get_songs_produced_url(),
            f"/api/artists/{self.tupac.id}/songs-produced",
        )

    def test_duplicate_artist_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Artist.objects.create(name="2Pac", hometown="New York, NY")

    def test_duplicate_artist_creation_case_insensitive_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Artist.objects.create(name="2pac")

    def test_artists_ordered_by_name(self):
        models.Artist.objects.create(name="Snoop Dogg", hometown="Long Beach, CA")
        models.Artist.objects.create(name="Dr. Dre", hometown="Compton, CA")
        artists = [str(artist) for artist in models.Artist.objects.all()]

        self.assertEqual(artists, ["2Pac", "Dr. Dre", "Snoop Dogg"])


class AlbumModelTestCase(TestCase):
    def setUp(self):
        self.all_eyez_on_me = models.Album.objects.create(
            title="All Eyez On Me",
            release_date=datetime.date(1996, 2, 13),
            label="Death Row Records",
            album_type="multidisc",
        )

    def test_album_creation_successful_title(self):
        self.assertEqual(self.all_eyez_on_me.title, "All Eyez On Me")

    def test_album_creation_successful_release_date(self):
        self.assertEqual(self.all_eyez_on_me.release_date, datetime.date(1996, 2, 13))

    def test_album_creation_successful_label(self):
        self.assertEqual(self.all_eyez_on_me.label, "Death Row Records")

    def test_album_creation_successful_album_type(self):
        self.assertEqual(self.all_eyez_on_me.album_type, "multidisc")

    def test_album_creation_without_label_successful(self):
        doggystyle = models.Album.objects.create(
            title="Doggystyle",
            release_date=datetime.date(1993, 11, 23),
            album_type="album",
        )

        self.assertEqual(doggystyle.label, "")

    def test_album_creation_without_album_type_successful(self):
        the_chronic = models.Album.objects.create(
            title="The Chronic",
            release_date=datetime.date(1992, 12, 15),
            label="Death Row Records",
        )

        self.assertEqual(the_chronic.album_type, "album")

    def test_album_title_max_length_is_600(self):
        max_length = self.all_eyez_on_me._meta.get_field("title").max_length

        self.assertEqual(max_length, 600)

    def test_album_artists_related_name_is_album_artists(self):
        related_name = self.all_eyez_on_me._meta.get_field("artists")._related_name

        self.assertEqual(related_name, "album_artists")

    def test_album_label_max_length_is_100(self):
        max_length = self.all_eyez_on_me._meta.get_field("label").max_length

        self.assertEqual(max_length, 100)

    def test_album_label_can_be_blank(self):
        blank = self.all_eyez_on_me._meta.get_field("label").blank

        self.assertTrue(blank)

    def test_album_album_type_max_length_is_10(self):
        max_length = self.all_eyez_on_me._meta.get_field("album_type").max_length

        self.assertEqual(max_length, 10)

    def test_album_album_type_has_three_choices(self):
        album_types = [
            ("album", "album"),
            ("multidisc", "multidisc"),
            ("single", "single"),
        ]
        type_choices = self.all_eyez_on_me._meta.get_field("album_type").choices

        self.assertEqual(album_types, type_choices)

    def test_album_str_method_returns_album_title(self):
        self.assertEqual(str(self.all_eyez_on_me), "All Eyez On Me")

    def test_album_get_url_method_returns_album_api_url(self):
        self.assertEqual(
            self.all_eyez_on_me.get_url(), f"/api/albums/{self.all_eyez_on_me.id}"
        )

    def test_album_get_songs_url_method_returns_album_songs_api_url(self):
        self.assertEqual(
            self.all_eyez_on_me.get_songs_url(),
            f"/api/albums/{self.all_eyez_on_me.id}/songs",
        )

    def test_duplicate_album_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Album.objects.create(
                title="All Eyez On Me",
                release_date=datetime.date(1996, 2, 13),
                album_type="album",
            )

    def test_duplicate_album_creation_case_insensitive_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Album.objects.create(
                title="all eyez on me", release_date=datetime.date(1996, 2, 13)
            )

    def test_albums_ordered_by_release_date(self):
        models.Album.objects.create(
            title="Necessary Roughness",
            release_date=datetime.date(1997, 6, 24),
            label="Death Row Records",
            album_type="album",
        )
        models.Album.objects.create(
            title="Dogg Food",
            release_date=datetime.date(1995, 10, 31),
            label="Death Row Records",
            album_type="album",
        )
        albums = [str(album) for album in models.Album.objects.all()]

        self.assertEqual(albums, ["Dogg Food", "All Eyez On Me", "Necessary Roughness"])


class AlbumArtistModelTestCase(TestCase):
    def setUp(self):
        self.kurupt = models.Artist.objects.create(
            name="Kurupt", hometown="Los Angeles, CA"
        )
        self.dogg_food = models.Album.objects.create(
            title="Dogg Food",
            release_date=datetime.date(1995, 10, 31),
            label="Death Row Records",
            album_type="album",
        )
        self.album_artist = models.AlbumArtist.objects.create(
            album=self.dogg_food, artist=self.kurupt
        )

    def test_album_artist_creation_successful_album(self):
        self.assertEqual(self.album_artist.album.title, "Dogg Food")

    def test_album_artist_creation_successful_artist(self):
        self.assertEqual(self.album_artist.artist.name, "Kurupt")

    def test_album_artist_str_method_returns_artist_name_album_title(self):
        self.assertEqual(str(self.album_artist), "Kurupt - Dogg Food")

    def test_duplicate_album_artist_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.AlbumArtist.objects.create(album=self.dogg_food, artist=self.kurupt)

    def test_album_artists_ordered_by_album_artist_id(self):
        tha_dogg_pound = models.Artist.objects.create(
            name="Tha Dogg Pound", hometown="Los Angeles, CA"
        )
        daz_dillinger = models.Artist.objects.create(
            name="Daz Dillinger", hometown="Long Beach, CA"
        )
        models.AlbumArtist.objects.create(album=self.dogg_food, artist=daz_dillinger)
        models.AlbumArtist.objects.create(album=self.dogg_food, artist=tha_dogg_pound)
        album_artists = [str(artist) for artist in models.AlbumArtist.objects.all()]
        expected_album_artist_order = [
            "Kurupt - Dogg Food",
            "Daz Dillinger - Dogg Food",
            "Tha Dogg Pound - Dogg Food",
        ]

        self.assertEqual(album_artists, expected_album_artist_order)


class SongModelTestCase(TestCase):
    def setUp(self):
        self.above_the_rim = models.Album.objects.create(
            title="Above The Rim Soundtrack",
            release_date=datetime.date(1994, 3, 22),
            label="Death Row Records",
            album_type="album",
        )
        self.gang_related = models.Album.objects.create(
            title="Gang Related Soundtrack",
            release_date=datetime.date(1997, 10, 7),
            label="Death Row Records",
            album_type="multidisc",
        )
        self.regulate = models.Song.objects.create(
            title="Regulate",
            album=self.above_the_rim,
            disc=1,
            track_number=7,
            length=251,
            path="/various-artists/above-the-rim-soundtrack/07_regulate.flac",
            play_count=5,
        )

    def test_song_creation_successful_title(self):
        self.assertEqual(self.regulate.title, "Regulate")

    def test_song_creation_successful_album(self):
        self.assertEqual(self.regulate.album.title, "Above The Rim Soundtrack")

    def test_song_creation_successful_disc(self):
        self.assertEqual(self.regulate.disc, 1)

    def test_song_creation_successful_track_number(self):
        self.assertEqual(self.regulate.track_number, 7)

    def test_song_creation_successful_length(self):
        self.assertEqual(self.regulate.length, 251)

    def test_song_creation_successful_path(self):
        self.assertEqual(
            self.regulate.path,
            "/various-artists/above-the-rim-soundtrack/07_regulate.flac",
        )

    def test_song_creation_successful_play_count(self):
        self.assertEqual(self.regulate.play_count, 5)

    def test_song_creation_without_disc_successful(self):
        way_too_major = models.Song.objects.create(
            title="Way Too Major",
            album=self.gang_related,
            track_number=1,
            length=327,
            path="/various-artists/gang-related-soundtrack/disc-1/01_way_too_major.flac",
            play_count=2,
        )

        self.assertEqual(way_too_major.disc, 1)

    def test_song_creation_without_play_count_successful(self):
        big_pimpin = models.Song.objects.create(
            title="Big Pimpin'",
            album=self.above_the_rim,
            track_number=4,
            length=238,
            path="/various-artists/above-the-rim-soundtrack/04_big_pimpin.flac",
        )

        self.assertEqual(big_pimpin.play_count, 0)

    def test_song_title_max_length_is_600(self):
        max_length = self.regulate._meta.get_field("title").max_length

        self.assertEqual(max_length, 600)

    def test_song_artists_related_name_is_song_artists(self):
        related_name = self.regulate._meta.get_field("artists")._related_name

        self.assertEqual(related_name, "song_artists")

    def test_song_producers_related_name_is_song_producers(self):
        related_name = self.regulate._meta.get_field("producers")._related_name

        self.assertEqual(related_name, "song_producers")

    def test_song_path_max_length_is_1000(self):
        max_length = self.regulate._meta.get_field("path").max_length

        self.assertEqual(max_length, 1000)

    def test_song_path_has_unique_constraint(self):
        unique_constraint = self.regulate._meta.get_field("path").unique

        self.assertTrue(unique_constraint)

    def test_song_str_method_returns_track_number_song_title_album_title(self):
        self.assertEqual(str(self.regulate), "7. Regulate [Above The Rim Soundtrack]")

    def test_song_get_url_method_returns_song_api_url(self):
        self.assertEqual(self.regulate.get_url(), f"/api/songs/{self.regulate.id}")

    def test_duplicate_song_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="regulate",
                album=self.above_the_rim,
                track_number=7,
                length=250,
                path="/various-artists/above-the-rim-soundtrack/07_regulate.flac",
                play_count=10,
            )

    def test_duplicate_song_creation_case_insensitive_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="Regulate",
                album=self.above_the_rim,
                track_number=7,
                length=251,
                path="/Various-Artists/Above-The-Rim-Soundtrack/07_Regulate.flac",
                play_count=10,
            )

    def test_song_creation_with_duplicate_track_number_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="Pour Out A Little Liquor",
                album=self.above_the_rim,
                track_number=7,
                length=210,
                path="/various-artists/above-the-rim-soundtrack/07_pour_out_a_little_liquor.flac",
            )

    def test_song_creation_with_invalid_disc_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="Get Yo Bang on",
                album=self.gang_related,
                disc=0,
                track_number=4,
                length=187,
                path="/various-artists/gang-related-soundtrack/disc-1/04_get_yo_bang_on.flac",
            )

    def test_song_creation_with_invalid_track_number_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="Pain",
                album=self.above_the_rim,
                track_number=0,
                length=274,
                path="/various-artists/above-the-rim-soundtrack/00_pain.flac",
            )

    def test_songs_ordered_by_play_count_release_date_disc_number_track_number(self):
        models.Song.objects.create(
            title="Afro Puffs",
            album=self.above_the_rim,
            track_number=10,
            length=290,
            path="/various-artists/above-the-rim-soundtrack/10_afro_puffs.flac",
        )
        models.Song.objects.create(
            title="Loc'd Out Hood",
            album=self.gang_related,
            disc=2,
            track_number=2,
            length=271,
            path="/various-artists/gang-related-soundtrack/disc-2/02_locd_out_hood.flac",
        )
        models.Song.objects.create(
            title="These Days",
            album=self.gang_related,
            disc=1,
            track_number=5,
            length=299,
            path="/various-artists/gang-related-soundtrack/disc-1/05_these_days.flac",
        )
        models.Song.objects.create(
            title="Staring Through My Rearview",
            album=self.gang_related,
            disc=1,
            track_number=8,
            length=312,
            path="/various-artists/gang-related-soundtrack/disc-1/08_staring_through_my_rearview.flac",
        )
        models.Song.objects.create(
            title="Made Niggaz",
            album=self.gang_related,
            disc=2,
            track_number=1,
            length=302,
            path="/various-artists/gang-related-soundtrack/disc-2/01_made_niggaz.flac",
            play_count=6,
        )
        songs = [str(song) for song in models.Song.objects.all()]
        expected_song_order = [
            "1. Made Niggaz [Gang Related Soundtrack]",
            "7. Regulate [Above The Rim Soundtrack]",
            "5. These Days [Gang Related Soundtrack]",
            "8. Staring Through My Rearview [Gang Related Soundtrack]",
            "2. Loc'd Out Hood [Gang Related Soundtrack]",
            "10. Afro Puffs [Above The Rim Soundtrack]",
        ]

        self.assertEqual(songs, expected_song_order)


class SongArtistModelTestCase(TestCase):
    def setUp(self):
        self.tha_dogg_pound = models.Artist.objects.create(name="Tha Dogg Pound")
        self.kurupt = models.Artist.objects.create(name="Kurupt")
        self.daz_dillinger = models.Artist.objects.create(name="Daz Dillinger")
        self.prince_ital_joe = models.Artist.objects.create(name="Prince Ital Joe")
        self.dogg_food = models.Album.objects.create(
            title="Dogg Food",
            release_date=datetime.date(1995, 10, 31),
            label="Death Row Records",
            album_type="album",
        )
        self.respect = models.Song.objects.create(
            title="Respect",
            album=self.dogg_food,
            track_number=3,
            length=354,
            path="/tha-dogg-pound/dogg-food/03_respect.flac",
        )
        self.song_artist = models.SongArtist.objects.create(
            song=self.respect, artist=self.kurupt, group=True
        )

    def test_song_artist_creation_successful_song(self):
        self.assertEqual(self.song_artist.song.title, "Respect")

    def test_song_artist_creation_successful_artist(self):
        self.assertEqual(self.song_artist.artist.name, "Kurupt")

    def test_song_artist_creation_successful_group(self):
        self.assertTrue(self.song_artist.group)

    def test_song_artist_creation_without_group_successful(self):
        song_feature = models.SongArtist.objects.create(
            song=self.respect, artist=self.tha_dogg_pound
        )

        self.assertFalse(song_feature.group)

    def test_song_artist_group_can_be_blank(self):
        blank = self.song_artist._meta.get_field("group").blank

        self.assertTrue(blank)

    def test_song_artist_str_method_returns_artist_name_song_title(self):
        self.assertEqual(str(self.song_artist), "Kurupt - Respect")

    def test_duplicate_song_artist_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.SongArtist.objects.create(
                song=self.respect, artist=self.kurupt, group=False
            )

    def test_song_artists_ordered_by_song_artist_id(self):
        models.SongArtist.objects.create(song=self.respect, artist=self.tha_dogg_pound)
        models.SongArtist.objects.create(song=self.respect, artist=self.prince_ital_joe)
        models.SongArtist.objects.create(
            song=self.respect, artist=self.daz_dillinger, group=True
        )
        song_artists = [str(artist) for artist in models.SongArtist.objects.all()]
        expected_song_artist_order = [
            "Kurupt - Respect",
            "Tha Dogg Pound - Respect",
            "Prince Ital Joe - Respect",
            "Daz Dillinger - Respect",
        ]

        self.assertEqual(song_artists, expected_song_artist_order)


class SongProducerModelTestCase(TestCase):
    def setUp(self):
        self.demetrius_shipp = models.Artist.objects.create(name="Demetrius Shipp")
        self.reggie_moore = models.Artist.objects.create(name="Reggie Moore")
        self.the_don_killuminati = models.Album.objects.create(
            title="The Don Killuminati: The 7 Day Theory",
            release_date=datetime.date(1996, 11, 5),
            label="Death Row Records",
            album_type="album",
        )
        self.toss_it_up = models.Song.objects.create(
            title="Toss It Up",
            album=self.the_don_killuminati,
            track_number=3,
            length=306,
            path="/2pac/the-don-killuminati-the-7-day-theory/03_toss_it_up.flac",
        )
        self.song_producer = models.SongProducer.objects.create(
            song=self.toss_it_up, producer=self.reggie_moore
        )

    def test_song_producer_creation_successful_song(self):
        self.assertEqual(self.song_producer.song.title, "Toss It Up")

    def test_song_producer_creation_successful_producer(self):
        self.assertEqual(self.song_producer.producer.name, "Reggie Moore")

    def test_song_producer_str_method_returns_producer_name_song_title(self):
        self.assertEqual(str(self.song_producer), "Reggie Moore - Toss It Up")

    def test_duplicate_song_producer_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.SongProducer.objects.create(
                song=self.toss_it_up, producer=self.reggie_moore
            )

    def test_song_producers_ordered_by_song_producer_id(self):
        models.SongProducer.objects.create(
            song=self.toss_it_up, producer=self.demetrius_shipp
        )
        song_producers = [
            str(producer) for producer in models.SongProducer.objects.all()
        ]
        expected_song_producer_order = [
            "Reggie Moore - Toss It Up",
            "Demetrius Shipp - Toss It Up",
        ]

        self.assertEqual(song_producers, expected_song_producer_order)
