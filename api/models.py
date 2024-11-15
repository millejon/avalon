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
