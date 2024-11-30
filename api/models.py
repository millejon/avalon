from django.db import models
from django.core import validators
from django.urls import reverse


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hometown = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def get_url(self) -> str:
        """Return artist API resource URL."""
        return reverse("api:retrieve_artist", args=[str(self.id)])

    def get_albums_url(self) -> str:
        """Return artist's albums API resource URL."""
        return reverse("api:retrieve_artist_albums", args=[str(self.id)])

    def get_singles_url(self) -> str:
        """Return artist's singles API resource URL."""
        return reverse("api:retrieve_artist_singles", args=[str(self.id)])

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower("name"),
                name="duplicate_artist_case_insensitive_match",
            ),
        ]


class Album(models.Model):
    ALBUM_TYPES = {"album": "album", "multidisc": "multidisc", "single": "single"}

    title = models.CharField(max_length=600)
    artists = models.ManyToManyField(
        Artist, through="AlbumArtist", related_name="album_artists"
    )
    release_date = models.DateField()
    label = models.CharField(max_length=100, blank=True)
    album_type = models.CharField(max_length=10, choices=ALBUM_TYPES, default="album")

    def __str__(self):
        return self.title

    def get_url(self) -> str:
        """Return album API resource URL."""
        return reverse("api:retrieve_album", args=[str(self.id)])

    def get_songs_url(self) -> str:
        """Return album's songs API resource URL."""
        return reverse("api:retrieve_album_songs", args=[str(self.id)])

    class Meta:
        ordering = ["release_date"]
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower("title"),
                "release_date",
                name="duplicate_album",
            ),
        ]


class AlbumArtist(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.artist.name} - {self.album.title}"

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["album", "artist"], name="duplicate_album_artist"
            )
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
    disc = models.PositiveSmallIntegerField(
        default=1, validators=[validators.MinValueValidator(1)]
    )
    track_number = models.PositiveSmallIntegerField(
        validators=[validators.MinValueValidator(1)]
    )
    length = models.PositiveSmallIntegerField()
    path = models.CharField(max_length=1000, unique=True)
    play_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.track_number}. {self.title} [{self.album.title}]"

    def get_url(self) -> str:
        """Return song API resource URL."""
        return reverse("api:retrieve_song", args=[str(self.id)])

    class Meta:
        ordering = ["-play_count", "-album__release_date", "disc", "track_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["album", "disc", "track_number"], name="duplicate_track_number"
            ),
            models.UniqueConstraint(
                models.functions.Lower("path"),
                name="duplicate_song_case_insensitive_match",
            ),
            models.CheckConstraint(
                condition=models.Q(disc__gte=1),
                name="disc_number_must_be_greater_than_0",
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
        return f"{self.artist.name} - {self.song.title}"

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

    def __str__(self):
        return f"{self.producer.name} - {self.song.title}"

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["song", "producer"], name="duplicate_producer"
            )
        ]
