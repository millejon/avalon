from typing import TypedDict, Optional

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
    albums: Optional[DiscogPreview]
    singles: Optional[DiscogPreview]
    songs: Optional[DiscogPreview]
    songs_produced: Optional[DiscogPreview]

    @staticmethod
    def resolve_url(obj):
        artist_url = reverse("api-1.0:retrieve_artist", kwargs={"id": obj.id})
        return obj.request.build_absolute_uri(artist_url)

    @staticmethod
    def resolve_albums(obj):
        albums = obj.album_set.filter(single=False)
        if albums:
            albums_url = reverse(
                "api-1.0:retrieve_artist_albums", kwargs={"id": obj.id}
            )
            return {
                "count": albums.count(),
                "url": obj.request.build_absolute_uri(albums_url),
            }
        else:
            return None

    @staticmethod
    def resolve_singles(obj):
        singles = obj.album_set.filter(single=True)
        if singles:
            singles_url = reverse(
                "api-1.0:retrieve_artist_singles", kwargs={"id": obj.id}
            )
            return {
                "count": singles.count(),
                "url": obj.request.build_absolute_uri(singles_url),
            }

    @staticmethod
    def resolve_songs(obj):
        songs = obj.feature_set.filter(producer=False)
        if songs:
            songs_url = reverse("api-1.0:retrieve_artist_songs", kwargs={"id": obj.id})
            return {
                "count": songs.count(),
                "url": obj.request.build_absolute_uri(songs_url),
            }
        else:
            return None

    @staticmethod
    def resolve_songs_produced(obj):
        produced = obj.feature_set.filter(producer=True)
        if produced:
            produced_url = reverse(
                "api-1.0:retrieve_artist_production_credits", kwargs={"id": obj.id}
            )
            return {
                "count": produced.count(),
                "url": obj.request.build_absolute_uri(produced_url),
            }
        else:
            return None
