from django.db import models
from django.core import validators
from django.urls import reverse


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_url(self) -> str:
        """Return the URL of the artist API resource."""
        return reverse("api-1.0:retrieve_artist", args=[str(self.id)])

    def get_albums_url(self) -> str:
        """Return the URL of the artist's albums API resource."""
        return reverse("api-1.0:retrieve_artist_albums", args=[str(self.id)])

    def get_singles_url(self) -> str:
        """Return the URL of the artist's singles API resource."""
        return reverse("api-1.0:retrieve_artist_singles", args=[str(self.id)])

    def get_songs_url(self) -> str:
        """Return the URL of the artist's songs API resource."""
        return reverse("api-1.0:retrieve_artist_songs", args=[str(self.id)])

    def get_credits_url(self) -> str:
        """Return the URL of the artist's production credits API resource."""
        return reverse(
            "api-1.0:retrieve_artist_production_credits", args=[str(self.id)]
        )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower("name"),
                name="duplicate_artist_case_insensitive_match",
            ),
        ]


class Album(models.Model):
    title = models.CharField(max_length=600)
    artists = models.ManyToManyField(
        Artist, through="AlbumArtist", related_name="album_artists"
    )
    release_date = models.DateField()
    single = models.BooleanField(default=False, blank=True)
    multidisc = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.title

    def get_url(self) -> str:
        """Return the URL of the album API resource."""
        return reverse("api-1.0:retrieve_album", args=[str(self.id)])

    def get_songs_url(self) -> str:
        """Return the URL of the album's songs API resource."""
        return reverse("api-1.0:retrieve_album_songs", args=[str(self.id)])

    class Meta:
        ordering = ["artists__name", "release_date"]
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower("title"),
                "release_date",
                name="duplicate_album",
            ),
            models.CheckConstraint(
                condition=~(models.Q(single=True) & models.Q(multidisc=True)),
                name="singles_can_not_be_multidisc",
            ),
        ]


class AlbumArtist(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.album.title} - {self.artist.name}"

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["album", "artist"], name="duplicate_album_artist"
            )
        ]


class Disc(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(
        validators=[validators.MinValueValidator(1)]
    )
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.album.title} ({self.title})"

    def get_url(self) -> str:
        """Return the URL of the disc API resource."""
        return reverse("api-1.0:retrieve_disc", args=[str(self.id)])

    class Meta:
        ordering = ["number"]
        constraints = [
            models.UniqueConstraint(
                fields=["album", "number"], name="duplicate_disc_number"
            ),
            models.UniqueConstraint(
                "album",
                models.functions.Lower("title"),
                name="duplicate_disc_title",
            ),
            models.CheckConstraint(
                condition=models.Q(number__gte=1),
                name="disc_number_must_be_greater_than_0",
            ),
        ]


class Song(models.Model):
    title = models.CharField(max_length=600)
    artists = models.ManyToManyField(
        Artist, through="SongArtist", related_name="song_artists"
    )
    producers = models.ManyToManyField(
        Artist, through="SongProducer", related_name="song_producers"
    )
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    disc = models.PositiveSmallIntegerField(null=True, blank=True)
    track_number = models.PositiveSmallIntegerField(
        validators=[validators.MinValueValidator(1)]
    )
    length = models.PositiveSmallIntegerField()
    path = models.CharField(max_length=1000, unique=True)
    play_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.track_number}. {self.title} [{self.album.title}]"

    def get_url(self) -> str:
        """Return the URL of the song API resource."""
        return reverse("api-1.0:retrieve_song", args=[str(self.id)])

    class Meta:
        ordering = ["-play_count", "-album__release_date", "disc", "track_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["album", "track_number"], name="duplicate_track_number"
            ),
            models.UniqueConstraint(
                models.functions.Lower("path"),
                name="duplicate_song_case_insensitive_match",
            ),
            models.CheckConstraint(
                condition=(models.Q(disc__gte=1) | models.Q(disc__isnull=True)),
                name="disc_number_must_be_greater_than_0_or_null",
            ),
            models.CheckConstraint(
                condition=models.Q(track_number__gte=1),
                name="track_number_must_be_greater_than_0",
            ),
        ]


class SongArtist(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    group = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.song.title} - {self.artist.name}"

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["song", "artist"], name="duplicate_song_artist"
            )
        ]


class SongProducer(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    producer = models.ForeignKey(Artist, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.song.title} - {self.producer.name} [{self.role}]"

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["song", "producer"], name="duplicate_producer"
            )
        ]
