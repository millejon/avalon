from django.db import models
from django.core import validators
from django.urls import reverse


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("view-artist", args=[str(self.id)])

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower("name"),
                name="artist_name_case_insensitive_unique",
                violation_error_message="Artist already exists (case insensitive match)",
            ),
        ]


class Album(models.Model):
    artists = models.ManyToManyField(Artist)
    title = models.CharField(max_length=600)
    release_date = models.DateField()
    single = models.BooleanField(default=False, blank=True)
    multidisc = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("view-album", args=[str(self.id)])

    class Meta:
        ordering = ["artists__name", "release_date"]
        constraints = [
            models.UniqueConstraint(fields=["title", "release_date"], name="unique_album")
        ]


class Disc(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    number = models.PositiveSmallIntegerField(validators=[validators.MinValueValidator(1)])

    def __str__(self):
        return f"{self.album.title} ({self.title})"

    class Meta:
        ordering = ["album__artists__name", "album__release_date", "number"]
        constraints = [
            models.UniqueConstraint(fields=["album", "number"], name="unique_disc"),
            models.CheckConstraint(
                check=models.Q(number__gte=1), name="disc_number_greater_than_0"
            ),
        ]


class Song(models.Model):
    artists = models.ManyToManyField(Artist, through="Feature")
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    disc = models.ForeignKey(Disc, on_delete=models.RESTRICT, null=True, blank=True)
    title = models.CharField(max_length=600)
    track_number = models.PositiveSmallIntegerField(validators=[validators.MinValueValidator(1)])
    length = models.PositiveIntegerField()
    play_count = models.PositiveIntegerField(default=0)
    path = models.CharField(max_length=1000, unique=True)

    def __str__(self):
        return f"{self.track_number}. {self.title} [{self.album.title}]"

    class Meta:
        ordering = ["-album__release_date", "disc__number", "track_number"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(track_number__gte=1), name="track_number_greater_than_0"
            )
        ]


class Feature(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    group = models.BooleanField(default=False, blank=True)
    producer = models.BooleanField(default=False, blank=True)
    role = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.artist.name} - {self.song.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["artist", "song", "group"], name="unique_vocalist"),
            models.UniqueConstraint(fields=["artist", "song", "producer"], name="unique_producer"),
        ]


class Playlist(models.Model):
    title = models.CharField(max_length=300, unique=True)
    songs = models.ManyToManyField(Song, through="PlaylistSong", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("view-playlist", args=[str(self.id)])

    class Meta:
        ordering = ["-last_modified"]
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower("title"),
                name="playlist_title_case_insensitive_unique",
                violation_error_message="Playlist already exists (case insensitive match)",
            ),
        ]


class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)


class Hub(models.Model):
    name = models.CharField(max_length=100, unique=True)
    artists = models.ManyToManyField(Artist, blank=True)
    albums = models.ManyToManyField(Album, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("view-hub", args=[str(self.id)])

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower("name"),
                name="hub_name_case_insensitive_unique",
                violation_error_message="Hub already exists (case insensitive match)",
            ),
        ]
