from datetime import date
from typing import TypedDict, List, Optional

from django.urls import reverse
from ninja import Schema, ModelSchema

from api import models


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
    # albums: Optional[DiscogPreview]
    # singles: Optional[DiscogPreview]
    # songs: Optional[DiscogPreview]
    # songs_produced: Optional[DiscogPreview]

    @staticmethod
    def resolve_url(obj, context):
        artist_url = reverse("api-1.0:retrieve_artist", kwargs={"id": obj.id})
        return context["request"].build_absolute_uri(artist_url)

    @staticmethod
    def resolve_albums(obj, context):
        albums = obj.album_set.filter(single=False)
        if albums:
            albums_url = reverse(
                "api-1.0:retrieve_artist_albums", kwargs={"id": obj.id}
            )
            return {
                "count": albums.count(),
                "url": context["request"].build_absolute_uri(albums_url),
            }

    @staticmethod
    def resolve_singles(obj, context):
        singles = obj.album_set.filter(single=True)
        if singles:
            singles_url = reverse(
                "api-1.0:retrieve_artist_singles", kwargs={"id": obj.id}
            )
            return {
                "count": singles.count(),
                "url": context["request"].build_absolute_uri(singles_url),
            }

    @staticmethod
    def resolve_songs(obj, context):
        songs = obj.feature_set.filter(producer=False)
        if songs:
            songs_url = reverse("api-1.0:retrieve_artist_songs", kwargs={"id": obj.id})
            return {
                "count": songs.count(),
                "url": context["request"].build_absolute_uri(songs_url),
            }

    @staticmethod
    def resolve_songs_produced(obj, context):
        produced = obj.feature_set.filter(producer=True)
        if produced:
            produced_url = reverse(
                "api-1.0:retrieve_artist_production_credits", kwargs={"id": obj.id}
            )
            return {
                "count": produced.count(),
                "url": context["request"].build_absolute_uri(produced_url),
            }


class ArtistBasics(Schema):
    id: int
    name: str
    url: str

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class AlbumIn(Schema):
    title: str
    release_date: date
    single: bool = False
    multidisc: bool = False


class AlbumOut(Schema):
    id: int
    title: str
    artists: List[ArtistBasics]
    tracklist: Optional[DiscogPreview]
    release_date: date
    single: bool
    multidisc: bool
    discs: Optional[DiscogPreview]
    url: str

    @staticmethod
    def resolve_tracklist(obj, context):
        if obj.song_set.all():
            return {
                "count": obj.song_set.count(),
                "url": context["request"].build_absolute_uri(obj.get_songs_url()),
            }

    @staticmethod
    def resolve_discs(obj, context):
        if obj.multidisc:
            return {
                "count": obj.disc_set.count(),
                "url": context["request"].build_absolute_uri(obj.get_discs_url()),
            }

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class AlbumBasics(Schema):
    id: int
    artists: List[ArtistBasics]
    title: str
    url: str

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())


class DiscIn(Schema):
    album: int
    title: str
    number: int


class DiscOut(Schema):
    id: int
    album: AlbumBasics
    title: str
    number: int
    url: str
    tracklist: Optional[DiscogPreview]

    @staticmethod
    def resolve_url(obj, context):
        disc_url = reverse("api-1.0:retrieve_disc", kwargs={"id": obj.id})
        return context["request"].build_absolute_uri(disc_url)

    @staticmethod
    def resolve_tracklist(obj, context):
        tracklist = obj.song_set.all()
        if tracklist:
            tracklist_url = reverse(
                "api-1.0:retrieve_disc_songs", kwargs={"id": obj.id}
            )
            return {
                "count": tracklist.count(),
                "url": context["request"].build_absolute_uri(tracklist_url),
            }


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


class SongProducerOut(Schema):
    song: SongBasics
    producer: ArtistBasics
    role: str


class SongProducerSummaryOut(Schema):
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


class SongProducersOut(Schema):
    id: int
    title: str
    producers: List[SongProducerSummaryOut]
    url: str

    @staticmethod
    def resolve_producers(obj):
        return obj.songproducer_set.all()

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())
