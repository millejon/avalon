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
                models.Lower("name"),
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
        ordering = ["artist__name", "release_date"]
        constraints = [
            models.UniqueConstraint(fields=["title", "release_date"], name="unique_album")
        ]


class Disc(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    number = models.PositiveSmallIntegerField(validators=[validators.MinValueValidator(1)])

    def __str__(self):
        return f"{self.album.name} ({self.title})"

    class Meta:
        ordering = ["album__artist__name", "album__release_date", "number"]
        constraints = [
            models.UniqueConstraint(fields=["album", "number"], name="unique_disc")
        ]


class Song(models.Model):
    artists = models.ManyToManyField(Artist, through="Feature")
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    disc = models.ForeignKey(Disc, on_delete=models.RESTRICT, null=True, blank=True)
    title = models.CharField(max_length=600)
    track_number = models.PositiveSmallIntegerField(validators=[validators.MinValueValidator(1)])
    length = models.PositiveIntegerField()
    play_count = models.PositiveIntegerField(default=0)
    path = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return f"{self.track_number}. {self.title} [{self.album.name}]"

    class Meta:
        ordering = ["-album__release_date", "disc__number", "track_number"]
