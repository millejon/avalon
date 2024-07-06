from typing import TypedDict

from django.urls import reverse
from ninja import Schema


class Error(Schema):
    error: str


class DiscogPreview(TypedDict):
    count: int
    url: str


class ArtistIn(Schema):
    name: str


class ArtistOut(Schema):
    id: int
    name: str
    url: str

    @staticmethod
    def resolve_url(obj):
        artist_url = reverse("api-1.0:retrieve_artist", kwargs={"id": obj.id})
        return obj.request.build_absolute_uri(artist_url)


class DetailedArtistOut(Schema):
    id: int
    name: str
    url: str
    albums: DiscogPreview
    singles: DiscogPreview
    songs: DiscogPreview
    songs_produced: DiscogPreview

    @staticmethod
    def resolve_url(obj):
        artist_url = reverse("api-1.0:retrieve_artist", kwargs={"id": obj.id})
        return obj.request.build_absolute_uri(artist_url)

    @staticmethod
    def resolve_albums(obj):
        albums_url = reverse("api-1.0:retrieve_artist_albums", kwargs={"id": obj.id})
        return {
            "count": obj.album_set.filter(single=False).count(),
            "url": obj.request.build_absolute_uri(albums_url),
        }

    @staticmethod
    def resolve_singles(obj):
        singles_url = reverse("api-1.0:retrieve_artist_singles", kwargs={"id": obj.id})
        return {
            "count": obj.album_set.filter(single=True).count(),
            "url": obj.request.build_absolute_uri(singles_url),
        }

    @staticmethod
    def resolve_songs(obj):
        songs_url = reverse("api-1.0:retrieve_artist_songs", kwargs={"id": obj.id})
        return {
            "count": obj.feature_set.filter(producer=False).count(),
            "url": obj.request.build_absolute_uri(songs_url),
        }

    @staticmethod
    def resolve_songs_produced(obj):
        produced_url = reverse(
            "api-1.0:retrieve_artist_production_credits", kwargs={"id": obj.id}
        )
        return {
            "count": obj.feature_set.filter(producer=True).count(),
            "url": obj.request.build_absolute_uri(produced_url),
        }
