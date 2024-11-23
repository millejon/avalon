from datetime import date
from typing import TypedDict

from ninja import Schema


class Preview(TypedDict):
    count: int
    url: str


class ArtistIn(Schema):
    name: str
    hometown: str = ""


class ArtistOutBasic(Schema):
    id: int
    name: str
    url: str

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class ArtistOut(Schema):
    id: int
    name: str
    hometown: str | None
    url: str

    @staticmethod
    def resolve_hometown(obj):
        return obj.hometown if obj.hometown else None

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class AlbumIn(Schema):
    title: str
    artists: list[ArtistIn]
    release_date: date
    label: str = ""
    album_type: str = "album"


class AlbumOut(Schema):
    id: int
    title: str
    artists: list[ArtistOutBasic]
    release_date: date
    label: str | None
    album_type: str
    tracklist: Preview | None
    url: str

    @staticmethod
    def resolve_label(obj):
        return obj.label if obj.label else None

    @staticmethod
    def resolve_tracklist(obj, context):
        if obj.song_set.all():
            return {
                "count": obj.song_set.count(),
                "url": context["request"].build_absolute_uri(obj.get_songs_url()),
            }
        else:
            return None

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())
