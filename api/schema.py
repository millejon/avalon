from datetime import date
from typing import TypedDict

from ninja import Schema


class Error(Schema):
    error: str


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
    albums: Preview
    singles: Preview
    url: str

    @staticmethod
    def resolve_hometown(obj):
        return obj.hometown if obj.hometown else None

    @staticmethod
    def resolve_albums(obj, context):
        return {
            "count": obj.album_artists.exclude(album_type="single").count(),
            "url": context["request"].build_absolute_uri(obj.get_albums_url()),
        }

    @staticmethod
    def resolve_singles(obj, context):
        return {
            "count": obj.album_artists.filter(album_type="single").count(),
            "url": context["request"].build_absolute_uri(obj.get_singles_url()),
        }

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class AlbumIn(Schema):
    title: str
    artists: list[ArtistIn]
    release_date: date
    label: str = ""
    album_type: str = "album"


class AlbumOutBasic(Schema):
    id: int
    title: str
    artists: list[ArtistOutBasic]
    release_date: date
    url: str

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class AlbumOut(Schema):
    id: int
    title: str
    artists: list[ArtistOutBasic]
    release_date: date
    label: str | None
    album_type: str
    # tracklist: Preview
    url: str

    @staticmethod
    def resolve_label(obj):
        return obj.label if obj.label else None

    # @staticmethod
    # def resolve_tracklist(obj, context):
    #     return {
    #         "count": obj.song_set.count(),
    #         "url": context["request"].build_absolute_uri(obj.get_songs_url()),
    #     }

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class SongIn(Schema):
    title: str
    artists: list[ArtistIn]
    group_members: list[ArtistIn]
    producers: list[ArtistIn]
    album: int
    disc: int = 1
    track_number: int
    length: int
    path: str


class SongOut(Schema):
    id: int
    title: str
    artists: list[ArtistOutBasic]
    group_members: list[ArtistOutBasic]
    producers: list[ArtistOutBasic]
    album: AlbumOutBasic
    disc: int
    track_number: int
    length: int
    path: str
    play_count: int
    url: str

    @staticmethod
    def resolve_artists(obj):
        features = obj.songartist_set.filter(group=False)
        return [feature.artist for feature in features]

    @staticmethod
    def resolve_group_members(obj):
        affiliations = obj.songartist_set.filter(group=True)
        return [affiliation.artist for affiliation in affiliations]

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())
