import datetime
import time

from django.test import TestCase
from django.db import IntegrityError

from api import models


class ArtistModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.nate_dogg = models.Artist.objects.create(name="Nate Dogg")

    def test_artist_creation_successful(self):
        self.assertEqual(self.nate_dogg.name, "Nate Dogg")

    def test_artist_name_max_length_is_100(self):
        max_length = self.nate_dogg._meta.get_field("name").max_length

        self.assertEqual(max_length, 100)

    def test_artist_name_unique_constraint_is_true(self):
        unique_constraint = self.nate_dogg._meta.get_field("name").unique

        self.assertTrue(unique_constraint)

    def test_str_method_returns_artist_name(self):
        self.assertEqual(str(self.nate_dogg), "Nate Dogg")

    def test_get_url_method_returns_artist_api_url(self):
        self.assertEqual(
            self.nate_dogg.get_url(), f"/api/v1/artists/{self.nate_dogg.id}"
        )

    def test_get_albums_url_method_returns_artist_albums_api_url(self):
        self.assertEqual(
            self.nate_dogg.get_albums_url(),
            f"/api/v1/artists/{self.nate_dogg.id}/albums",
        )

    def test_get_singles_url_method_returns_artist_singles_api_url(self):
        self.assertEqual(
            self.nate_dogg.get_singles_url(),
            f"/api/v1/artists/{self.nate_dogg.id}/singles",
        )

    def test_get_songs_url_method_returns_artist_songs_api_url(self):
        self.assertEqual(
            self.nate_dogg.get_songs_url(), f"/api/v1/artists/{self.nate_dogg.id}/songs"
        )

    def test_get_credits_url_method_returns_artist_production_credits_api_url(self):
        self.assertEqual(
            self.nate_dogg.get_credits_url(),
            f"/api/v1/artists/{self.nate_dogg.id}/produced",
        )

    def test_duplicate_artist_creation_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Artist.objects.create(name="Nate Dogg")

    def test_duplicate_artist_creation_case_insensitive_unsuccessful(self):
        with self.assertRaises(IntegrityError):
            models.Artist.objects.create(name="nate dogg")

    def test_artists_ordered_by_name(self):
        models.Artist.objects.create(name="Warren G")
        models.Artist.objects.create(name="Luniz")
        artists = [str(artist) for artist in models.Artist.objects.all()]

        self.assertEqual(artists, ["Luniz", "Nate Dogg", "Warren G"])


class AlbumModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.the_chronic = models.Album.objects.create(
            title="The Chronic",
            release_date=datetime.date(1992, 12, 15),
        )

    def test_album_creation(self):
        self.assertEqual(self.the_chronic.title, "The Chronic")
        self.assertEqual(self.the_chronic.release_date, datetime.date(1992, 12, 15))

    def test_album_creation_single_false_by_default(self):
        self.assertFalse(self.the_chronic.single)

    def test_album_creation_multidisc_false_by_default(self):
        self.assertFalse(self.the_chronic.multidisc)

    def test_title_max_length(self):
        max_length = self.the_chronic._meta.get_field("title").max_length

        self.assertEqual(max_length, 600)

    def test_album_str_method(self):
        self.assertEqual(str(self.the_chronic), "The Chronic")

    def test_album_get_url_method(self):
        self.assertTrue(
            self.the_chronic.get_url().endswith(f"/api/v1/albums/{self.the_chronic.id}")
        )

    def test_album_creation_duplicate_album(self):
        with self.assertRaises(IntegrityError):
            models.Album.objects.create(
                title="The Chronic",
                release_date=datetime.date(1992, 12, 15),
            )

    def test_album_creation_multidisc_single(self):
        with self.assertRaises(IntegrityError):
            models.Album.objects.create(
                title="Deep Cover",
                release_date=datetime.date(1992, 4, 9),
                single=True,
                multidisc=True,
            )

    def test_album_ordering(self):
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
        expected_album_order = [
            "The Chronic",
            "Doggystyle",
            "Tha Doggfather",
        ]

        self.assertEqual(albums, expected_album_order)


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

    def test_album_artist_creation(self):
        self.assertEqual(self.album_artist.album.title, "Blaqkout")
        self.assertEqual(self.album_artist.artist.name, "Kurupt")

    def test_album_artist_str_method(self):
        self.assertEqual(str(self.album_artist), "Blaqkout - Kurupt")

    def test_album_artist_ordering(self):
        models.AlbumArtist.objects.create(album=self.blaqkout, artist=self.dj_quik)

        album_artists = [str(artist) for artist in models.AlbumArtist.objects.all()]
        expected_artist_order = ["Blaqkout - Kurupt", "Blaqkout - DJ Quik"]

        self.assertEqual(album_artists, expected_artist_order)


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

    def test_disc_creation(self):
        self.assertEqual(self.book2.album.title, "All Eyez On Me")
        self.assertEqual(self.book2.number, 2)
        self.assertEqual(self.book2.title, "Book 2")

    def test_title_max_length(self):
        max_length = self.book2._meta.get_field("title").max_length

        self.assertEqual(max_length, 100)

    def test_disc_str_method(self):
        self.assertEqual(str(self.book2), "All Eyez On Me (Book 2)")

    def test_disc_get_url_method(self):
        self.assertTrue(self.book2.get_url().endswith(f"/api/v1/discs/{self.book2.id}"))

    def test_disc_creation_duplicate_disc(self):
        with self.assertRaises(IntegrityError):
            models.Disc.objects.create(
                album=self.all_eyez_on_me,
                number=2,
                title="Book 2",
            )

    def test_disc_creation_invalid_disc_number(self):
        with self.assertRaises(IntegrityError):
            models.Disc.objects.create(
                album=self.all_eyez_on_me,
                number=0,
                title="Book 0",
            )

    def test_disc_ordering(self):
        models.Disc.objects.create(album=self.all_eyez_on_me, number=1, title="Book 1")

        discs = [str(disc) for disc in models.Disc.objects.all()]
        expected_disc_order = [
            "All Eyez On Me (Book 1)",
            "All Eyez On Me (Book 2)",
        ]

        self.assertEqual(discs, expected_disc_order)


class SongModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.illmatic = models.Album.objects.create(
            title="Illmatic",
            release_date=datetime.date(1994, 4, 19),
        )
        cls.streets_disciple = models.Album.objects.create(
            title="Street's Disciple",
            release_date=datetime.date(2004, 11, 30),
            multidisc=True,
        )
        cls.ny_state_of_mind = models.Song.objects.create(
            title="N.Y. State Of Mind",
            album=cls.illmatic,
            track_number=2,
            length=293,
            path="/nas/illmatic/02_ny_state_of_mind.flac",
        )

    def test_song_creation(self):
        self.assertEqual(self.ny_state_of_mind.title, "N.Y. State Of Mind")
        self.assertEqual(self.ny_state_of_mind.album.title, "Illmatic")
        self.assertEqual(self.ny_state_of_mind.track_number, 2)
        self.assertEqual(self.ny_state_of_mind.length, 293)
        self.assertEqual(
            self.ny_state_of_mind.path, "/nas/illmatic/02_ny_state_of_mind.flac"
        )

    def test_song_creation_disc_null_by_default(self):
        self.assertIsNone(self.ny_state_of_mind.disc)

    def test_song_creation_play_count_zero_by_default(self):
        self.assertEqual(self.ny_state_of_mind.play_count, 0)

    def test_title_max_length(self):
        max_length = self.ny_state_of_mind._meta.get_field("title").max_length

        self.assertEqual(max_length, 600)

    def test_path_max_length(self):
        max_length = self.ny_state_of_mind._meta.get_field("path").max_length

        self.assertEqual(max_length, 1000)

    def test_song_str_method(self):
        self.assertEqual(str(self.ny_state_of_mind), "2. N.Y. State Of Mind [Illmatic]")

    def test_song_get_url_method(self):
        self.assertTrue(
            self.ny_state_of_mind.get_url().endswith(
                f"/api/v1/songs/{self.ny_state_of_mind.id}"
            )
        )

    def test_song_creation_duplicate_song(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="New York State Of Mind",
                album=self.illmatic,
                track_number=2,
                length=295,
                path="/nas/illmatic/02_ny_state_of_mind.flac",
            )

    def test_song_creation_invalid_disc_number(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="Nazareth Savage",
                album=self.streets_disciple,
                disc=0,
                track_number=3,
                length=160,
                path="/nas/streets-disciple/disc-1/03_nazareth_savage.flac",
            )

    def test_song_creation_invalid_track_number(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="I'm A Villain",
                album=self.illmatic,
                track_number=0,
                length=270,
                path="/nas/illmatic/00_im_a_villain.flac",
            )

    def test_song_creation_invalid_play_count(self):
        with self.assertRaises(IntegrityError):
            models.Song.objects.create(
                title="Life's A Bitch",
                album=self.illmatic,
                track_number=3,
                length=210,
                path="/nas/illmatic/03_lifes_a_bitch.flac",
                play_count=-1,
            )

    def test_song_ordering(self):
        models.Song.objects.create(
            title="It Ain't Hard To Tell",
            album=self.illmatic,
            track_number=10,
            length=202,
            path="/nas/illmatic/10_it_aint_hard_to_tell.flac",
            play_count=3,
        )
        models.Song.objects.create(
            title="Suicide Bounce",
            album=self.streets_disciple,
            disc=2,
            track_number=1,
            length=237,
            path="/nas/streets-disciple/disc-2/01_suicide_bounce.flac",
        )
        models.Song.objects.create(
            title="Disciple",
            album=self.streets_disciple,
            disc=1,
            track_number=6,
            length=180,
            path="/nas/streets-disciple/disc-1/06_disciple.flac",
        )

        songs = [str(song) for song in models.Song.objects.all()]
        expected_song_order = [
            "10. It Ain't Hard To Tell [Illmatic]",
            "6. Disciple [Street's Disciple]",
            "1. Suicide Bounce [Street's Disciple]",
            "2. N.Y. State Of Mind [Illmatic]",
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

    def test_song_artist_creation(self):
        self.assertEqual(self.song_artist.song.title, "Smooth")
        self.assertEqual(self.song_artist.artist.name, "Tha Dogg Pound")

    def test_song_artist_creation_group_false_by_default(self):
        self.assertFalse(self.song_artist.group)

    def test_song_artist_str_method(self):
        self.assertEqual(str(self.song_artist), "Smooth - Tha Dogg Pound")

    def test_song_artist_creation_group_member(self):
        group_feature = models.SongArtist.objects.create(
            song=self.smooth, artist=self.kurupt, group=True
        )

        self.assertEqual(group_feature.song.title, "Smooth")
        self.assertEqual(group_feature.artist.name, "Kurupt")
        self.assertTrue(group_feature.group)

    def test_song_artist_creation_nonunique_group_member(self):
        with self.assertRaises(IntegrityError):
            models.SongArtist.objects.create(
                song=self.smooth, artist=self.tha_dogg_pound, group=True
            )

    def test_song_artist_ordering(self):
        models.SongArtist.objects.create(song=self.smooth, artist=self.snoop_dogg)
        models.SongArtist.objects.create(
            song=self.smooth, artist=self.kurupt, group=True
        )
        models.SongArtist.objects.create(song=self.smooth, artist=self.val_young)

        song_artists = [str(artist) for artist in models.SongArtist.objects.all()]
        expected_artist_order = [
            "Smooth - Tha Dogg Pound",
            "Smooth - Snoop Dogg",
            "Smooth - Kurupt",
            "Smooth - Val Young",
        ]

        self.assertEqual(song_artists, expected_artist_order)


class SongProducerModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fourth_disciple = models.Artist.objects.create(name="4th Disciple")
        cls.rza = models.Artist.objects.create(name="RZA")
        cls.wu_tang_forever = models.Album.objects.create(
            title="Wu-Tang Forever",
            release_date=datetime.date(1997, 6, 3),
            multidisc=True,
        )
        cls.impossible = models.Song.objects.create(
            title="Impossible",
            album=cls.wu_tang_forever,
            disc=2,
            track_number=3,
            length=268,
            path="/wu-tang-clan/wu-tang-forever/disc-2/03_impossible.flac",
        )
        cls.song_producer = models.SongProducer.objects.create(
            song=cls.impossible, producer=cls.rza, role="Co-Producer"
        )

    def test_song_producer_creation(self):
        self.assertEqual(self.song_producer.song.title, "Impossible")
        self.assertEqual(self.song_producer.producer.name, "RZA")
        self.assertEqual(self.song_producer.role, "Co-Producer")

    def test_role_max_length(self):
        max_length = self.song_producer._meta.get_field("role").max_length

        self.assertEqual(max_length, 100)

    def test_song_producer_str_method(self):
        self.assertEqual(str(self.song_producer), "Impossible - RZA [Co-Producer]")

    def test_nonunique_song_producer_creation(self):
        with self.assertRaises(IntegrityError):
            models.SongProducer.objects.create(
                song=self.impossible, producer=self.rza, role="Producer"
            )

    def test_song_producer_ordering(self):
        models.SongProducer.objects.create(
            song=self.impossible, producer=self.fourth_disciple, role="Producer"
        )

        producers = [str(producer) for producer in models.SongProducer.objects.all()]
        expected_producer_order = [
            "Impossible - RZA [Co-Producer]",
            "Impossible - 4th Disciple [Producer]",
        ]

        self.assertEqual(producers, expected_producer_order)


class PlaylistModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.playlist = models.Playlist.objects.create(title="Rock The Bells")

    def test_playlist_creation(self):
        self.assertEqual(self.playlist.title, "Rock The Bells")
        self.assertIsNotNone(self.playlist.created)
        self.assertIsNotNone(self.playlist.last_modified)

    def test_playlist_creation_songs_null_by_default(self):
        self.assertEqual(self.playlist.songs.count(), 0)

    def test_title_max_length(self):
        max_length = self.playlist._meta.get_field("title").max_length

        self.assertEqual(max_length, 300)

    def test_playlist_str_method(self):
        self.assertEqual(str(self.playlist), "Rock The Bells")

    def test_playlist_get_absolute_url(self):
        # TODO: Add test after coding front-end views
        pass

    def test_nonunique_playlist_creation(self):
        with self.assertRaises(IntegrityError):
            models.Playlist.objects.create(title="Rock The Bells")

    def test_nonunique_playlist_creation_case_insensitive(self):
        with self.assertRaises(IntegrityError):
            models.Playlist.objects.create(title="rock the bells")

    def test_playlist_ordering(self):
        playlist2 = models.Playlist.objects.create(title="Kaleidoscope Dreams")
        time.sleep(0.1)
        models.Playlist.objects.create(title="Computer Love")
        time.sleep(0.1)
        album = models.Album.objects.create(
            title="Ready To Die", release_date=datetime.date(1994, 9, 13)
        )
        song = models.Song.objects.create(
            album=album,
            title="Machine Gun Funk",
            track_number=4,
            length=257,
            path="D:/Music/the-notorious-big/ready-to-die/04_machine_gun_funk.flac",
        )
        playlist2.songs.add(song)
        playlist2.save()

        playlists = [str(playlist) for playlist in models.Playlist.objects.all()]

        self.assertEqual(
            playlists, ["Kaleidoscope Dreams", "Computer Love", "Rock The Bells"]
        )


class PlaylistSongModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.playlist = models.Playlist.objects.create(title="Murda Muzik")
        cls.album = models.Album.objects.create(
            title="Enter The Wu-Tang (36 Chambers)",
            release_date=datetime.date(1993, 11, 9),
        )
        cls.song = models.Song.objects.create(
            album=cls.album,
            title="Protect Ya Neck",
            track_number=10,
            length=292,
            path="D:/Music/wutang-clan/enter-the-wutang-36-chambers/10_protect_ya_neck.flac",
        )
        cls.playlist_song = models.PlaylistSong.objects.create(
            playlist=cls.playlist, song=cls.song
        )

    def test_playlist_song_creation(self):
        self.assertEqual(self.playlist.title, "Murda Muzik")
        self.assertEqual(self.song.title, "Protect Ya Neck")
        self.assertIsNotNone(self.playlist_song.date_added)

    def test_playlist_song_str_method(self):
        self.assertEqual(str(self.playlist_song), "Protect Ya Neck [Murda Muzik]")


class HubModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hub = models.Hub.objects.create(name="Death Row Records")

    def test_hub_creation(self):
        self.assertEqual(self.hub.name, "Death Row Records")

    def test_hub_creation_artists_null_by_default(self):
        self.assertEqual(self.hub.artists.count(), 0)

    def test_hub_creation_albums_null_by_default(self):
        self.assertEqual(self.hub.albums.count(), 0)

    def test_name_max_length(self):
        max_length = self.hub._meta.get_field("name").max_length

        self.assertEqual(max_length, 100)

    def test_hub_str_method(self):
        self.assertEqual(str(self.hub), "Death Row Records")

    def test_hub_get_absolute_url(self):
        # TODO: Add test after coding front-end views
        pass

    def test_nonunique_hub_creation(self):
        with self.assertRaises(IntegrityError):
            models.Hub.objects.create(name="Death Row Records")

    def test_nonunique_hub_creation_case_insensitive(self):
        with self.assertRaises(IntegrityError):
            models.Hub.objects.create(name="DEATH ROW Records")

    def test_hub_ordering(self):
        models.Hub.objects.create(name="Roc-A-Fella Records")
        models.Hub.objects.create(name="Griselda")

        hubs = [str(hub) for hub in models.Hub.objects.all()]

        self.assertEqual(hubs, ["Death Row Records", "Griselda", "Roc-A-Fella Records"])
