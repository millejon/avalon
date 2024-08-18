from datetime import date
from typing import TypedDict, List, Optional

from ninja import Schema, ModelSchema

from api import models


class Error(Schema):
    error: str


class CatalogPreview(TypedDict):
    count: int
    url: str


class ArtistIn(ModelSchema):
    class Meta:
        model = models.Artist
        fields = ["name"]


class Artist(Schema):
    id: int
    name: str
    albums: Optional[CatalogPreview]
    singles: Optional[CatalogPreview]
    songs: Optional[CatalogPreview]
    production_credits: Optional[CatalogPreview]
    url: str

    @staticmethod
    def resolve_albums(obj, context):
        albums = obj.albumartist_set.filter(album__single=False)
        if albums:
            return {
                "count": albums.count(),
                "url": context["request"].build_absolute_uri(obj.get_albums_url()),
            }

    @staticmethod
    def resolve_singles(obj, context):
        singles = obj.albumartist_set.filter(album__single=True)
        if singles:
            return {
                "count": singles.count(),
                "url": context["request"].build_absolute_uri(obj.get_singles_url()),
            }

    @staticmethod
    def resolve_songs(obj, context):
        songs = obj.songartist_set.all()
        if songs:
            return {
                "count": songs.count(),
                "url": context["request"].build_absolute_uri(obj.get_songs_url()),
            }

    @staticmethod
    def resolve_production_credits(obj, context):
        credits = obj.songproducer_set.all()
        if credits:
            return {
                "count": credits.count(),
                "url": context["request"].build_absolute_uri(obj.get_credits_url()),
            }

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class ArtistBasics(Schema):
    id: int
    name: str
    url: str

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class AlbumIn(ModelSchema):
    class Meta:
        model = models.Album
        fields = ["title", "release_date", "single", "multidisc"]
        fields_optional = ["single", "multidisc"]


class AlbumBasics(Schema):
    id: int
    artists: List[ArtistBasics]
    title: str
    url: str

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class DiscIn(ModelSchema):
    class Meta:
        model = models.Disc
        fields = ["album", "number", "title"]
        fields_optional = ["album"]


class Disc(Schema):
    id: int
    album: AlbumBasics
    number: int
    title: str
    url: str

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class DiscBasics(Schema):
    id: int
    number: int
    title: str
    url: str

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class Album(Schema):
    id: int
    title: str
    artists: List[ArtistBasics]
    tracklist: Optional[CatalogPreview]
    release_date: date
    single: bool
    multidisc: bool
    discs: Optional[List[DiscBasics]]
    url: str

    @staticmethod
    def resolve_tracklist(obj, context):
        if obj.song_set.all():
            return {
                "count": obj.song_set.count(),
                "url": context["request"].build_absolute_uri(obj.get_songs_url()),
            }

    @staticmethod
    def resolve_discs(obj):
        if obj.multidisc:
            return obj.disc_set.all()

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class AlbumArtistIn(ModelSchema):
    class Meta:
        model = models.AlbumArtist
        fields = ["artist"]


class SongIn(ModelSchema):
    class Meta:
        model = models.Song
        fields = ["title", "album", "disc", "track_number", "length", "path"]
        fields_optional = ["disc"]


class Song(Schema):
    id: int
    title: str
    artists: List[ArtistBasics]
    producers: List[ArtistBasics]
    album: AlbumBasics
    disc: Optional[int]
    track_number: int
    length: int
    path: str
    play_count: int
    url: str

    @staticmethod
    def resolve_artists(obj):
        artists = obj.songartist_set.filter(group=False)
        return [feature.artist for feature in artists]

    @staticmethod
    def resolve_producers(obj):
        producers = obj.songproducer_set.filter(role="Producer")
        return [feature.producer for feature in producers]

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class SongBasics(Schema):
    id: int
    title: str
    url: str

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class SongArtistIn(ModelSchema):
    class Meta:
        model = models.SongArtist
        fields = ["artist", "group"]
        fields_optional = ["group"]


class SongArtist(Schema):
    song: SongBasics
    artist: ArtistBasics
    group: bool


class SongArtistDetails(Schema):
    id: int
    name: str
    group: bool
    url: str

    @staticmethod
    def resolve_id(obj):
        return obj.artist.id

    @staticmethod
    def resolve_name(obj):
        return obj.artist.name

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.artist.get_url())


class SongArtists(Schema):
    id: int
    title: str
    artists: List[SongArtistDetails]
    url: str

    @staticmethod
    def resolve_artists(obj):
        return obj.songartist_set.all()

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class SongProducerIn(ModelSchema):
    class Meta:
        model = models.SongProducer
        fields = ["producer", "role"]


class SongProducer(Schema):
    song: SongBasics
    producer: ArtistBasics
    role: str


class SongProducerDetails(Schema):
    id: int
    name: str
    role: str
    url: str

    @staticmethod
    def resolve_id(obj):
        return obj.producer.id

    @staticmethod
    def resolve_name(obj):
        return obj.producer.name

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.producer.get_url())


class SongProducers(Schema):
    id: int
    title: str
    producers: List[SongProducerDetails]
    url: str

    @staticmethod
    def resolve_producers(obj):
        return obj.songproducer_set.all()

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())
