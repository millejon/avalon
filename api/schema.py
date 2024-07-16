from datetime import date
from typing import TypedDict, List, Optional

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
    albums: Optional[DiscogPreview]
    singles: Optional[DiscogPreview]
    songs: Optional[DiscogPreview]
    songs_produced: Optional[DiscogPreview]

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


class ArtistSummaryOut(Schema):
    id: int
    name: str
    url: str

    @staticmethod
    def resolve_url(obj, context):
        artist_url = reverse("api-1.0:retrieve_artist", kwargs={"id": obj.id})
        return context["request"].build_absolute_uri(artist_url)


class AlbumIn(Schema):
    artists: List[int]
    title: str
    release_date: date
    single: bool = False
    multidisc: bool = False


class AlbumOut(Schema):
    id: int
    artists: List[ArtistSummaryOut]
    title: str
    release_date: date
    single: bool
    multidisc: bool
    url: str
    tracklist: Optional[DiscogPreview]
    discs: Optional[DiscogPreview]

    @staticmethod
    def resolve_url(obj, context):
        album_url = reverse("api-1.0:retrieve_album", kwargs={"id": obj.id})
        return context["request"].build_absolute_uri(album_url)

    @staticmethod
    def resolve_tracklist(obj, context):
        tracklist = obj.song_set.all()
        if tracklist:
            tracklist_url = reverse(
                "api-1.0:retrieve_album_songs", kwargs={"id": obj.id}
            )
            return {
                "count": tracklist.count(),
                "url": context["request"].build_absolute_uri(tracklist_url),
            }

    @staticmethod
    def resolve_discs(obj, context):
        if obj.multidisc:
            discs_url = reverse("api-1.0:retrieve_album_discs", kwargs={"id": obj.id})
            return {
                "count": obj.disc_set.count(),
                "url": context["request"].build_absolute_uri(discs_url),
            }


class AlbumSummaryOut(Schema):
    id: int
    artists: List[ArtistSummaryOut]
    title: str
    url: str

    @staticmethod
    def resolve_url(obj, context):
        album_url = reverse("api-1.0:retrieve_album", kwargs={"id": obj.id})
        return context["request"].build_absolute_uri(album_url)


class MiniAlbumSummaryOut(Schema):
    id: int
    title: str
    url: str

    @staticmethod
    def resolve_url(obj, context):
        album_url = reverse("api-1.0:retrieve_album", kwargs={"id": obj.id})
        return context["request"].build_absolute_uri(album_url)


class DiscIn(Schema):
    album: int
    title: str
    number: int


class DiscOut(Schema):
    id: int
    album: MiniAlbumSummaryOut
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


class SongIn(Schema):
    album: int
    disc: int = None
    title: str
    track_number: int
    length: int
    path: str


class SongOut(Schema):
    id: int
    artists: List[ArtistSummaryOut]
    album: MiniAlbumSummaryOut
    disc: Optional[int]
    track_number: int
    title: str
    length: int
    play_count: int
    path: str
    url: str

    @staticmethod
    def resolve_url(obj, context):
        song_url = reverse("api-1.0:retrieve_song", kwargs={"id": obj.id})
        return context["request"].build_absolute_uri(song_url)

    @staticmethod
    def resolve_disc(obj):
        return obj.disc.number if obj.disc else None


class SongSummaryOut(Schema):
    id: int
    artists: List[str]
    album: str
    title: str
    url: str

    @staticmethod
    def resolve_url(obj, context):
        song_url = reverse("api-1.0:retrieve_song", kwargs={"id": obj.id})
        return context["request"].build_absolute_uri(song_url)

    @staticmethod
    def resolve_artists(obj):
        return [artist.name for artist in obj.artists.all()]

    @staticmethod
    def resolve_album(obj):
        return obj.album.title
