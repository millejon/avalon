from django.db import models
from django.urls import reverse


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hometown = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def get_url(self) -> str:
        """Return artist API resource URL."""
        return reverse("api:retrieve_artist", args=[str(self.id)])

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
