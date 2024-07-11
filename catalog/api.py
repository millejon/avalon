from collections import OrderedDict
from typing import List

from ninja import NinjaAPI

from catalog import models, schema
from catalog import utilities as util

api = NinjaAPI(version="1.0")


@api.post("artists/", response={201: schema.DetailedArtistOut}, tags=["artists"])
def create_artist(request, data: schema.ArtistIn):
    data = util.strip_whitespace(data.dict())
    artist = models.Artist.objects.create(**data)
    return 201, artist


@api.get(
    "artists/{int:id}",
    response={200: schema.DetailedArtistOut, 404: schema.Error},
    tags=["artists"],
)
def retrieve_artist(request, id: int):
    try:
        artist = models.Artist.objects.get(pk=id)
        return 200, artist
    except models.Artist.DoesNotExist:
        return 404, {"error": f"Artist with id = {id} does not exist."}


@api.put(
    "artists/{int:id}",
    response={200: schema.DetailedArtistOut, 404: schema.Error},
    tags=["artists"],
)
def update_artist(request, id: int, data: schema.ArtistIn):
    try:
        artist = models.Artist.objects.get(pk=id)
        data = util.strip_whitespace(data.dict())
        for attr, value in data.items():
            setattr(artist, attr, value)
        artist.save()
        return 200, artist
    except models.Artist.DoesNotExist:
        return 404, {"error": f"Artist with id = {id} does not exist."}


@api.delete(
    "artists/{int:id}", response={204: None, 404: schema.Error}, tags=["artists"]
)
def delete_artist(request, id: int):
    try:
        artist = models.Artist.objects.get(pk=id)
        artist.delete()
        return 204, None
    except models.Artist.DoesNotExist:
        return 404, {"error": f"Artist with id = {id} does not exist."}


# TODO: Write tests for this endpoint after finishing album endpoints
@api.get("artists/", response={200: List[schema.ArtistOut]}, tags=["artists"])
def retrieve_all_artists(request):
    artists = models.Artist.objects.filter(album__isnull=False).distinct("name")
    return 200, artists


@api.get("artists/{int:id}/albums/")
def retrieve_artist_albums(request, id: int):
    pass


@api.get("artists/{int:id}/singles/")
def retrieve_artist_singles(request, id: int):
    pass


@api.get("artists/{int:id}/songs/")
def retrieve_artist_songs(request, id: int):
    pass


@api.get("artists/{int:id}/produced/")
def retrieve_artist_production_credits(request, id: int):
    pass


@api.post("albums/", response={201: schema.DetailedAlbumOut}, tags=["albums"])
def create_album(request, data: schema.AlbumIn):
    data = util.strip_whitespace(data.dict())
    artists = data.pop("artists")

    album = models.Album.objects.create(**data)
    for artist in artists:
        album.artists.add(artist)
    album.save()

    return 201, album


@api.get(
    "albums/{int:id}",
    response={200: schema.DetailedAlbumOut, 404: schema.Error},
    tags=["albums"],
)
def retrieve_album(request, id: int):
    try:
        album = models.Album.objects.get(pk=id)
        return 200, album
    except models.Album.DoesNotExist:
        return 404, {"error": f"Album with id = {id} does not exist."}


@api.put(
    "albums/{int:id}",
    response={200: schema.DetailedAlbumOut, 404: schema.Error},
    tags=["albums"],
)
def update_album(request, id: int, data: schema.AlbumIn):
    try:
        album = models.Album.objects.get(pk=id)
        data = util.strip_whitespace(data.dict())
        artists = data.pop("artists")

        for attr, value in data.items():
            setattr(album, attr, value)
        for artist in artists:
            album.artists.add(artist)
        album.save()

        return 200, album
    except models.Album.DoesNotExist:
        return 404, {"error": f"Album with id = {id} does not exist."}


@api.delete("albums/{int:id}", response={204: None, 404: schema.Error}, tags=["albums"])
def delete_album(request, id: int):
    try:
        album = models.Album.objects.get(pk=id)
        album.delete()
        return 204, None
    except models.Album.DoesNotExist:
        return 404, {"error": f"Album with id = {id} does not exist."}


# TODO: Need to figure out how to order albums by first artist added to
# TODO: album, not just first alphabetical album artist, then write
# TODO: tests for this endpoint.
@api.get("albums/", response={200: List[schema.AlbumOut]}, tags=["albums"])
def retrieve_all_albums(request):
    albums = models.Album.objects.filter(single=False)

    # Since albums are ordered by a field from a related model (artist
    # name), filter() returns duplicate model instances when an album
    # has multiple album artists, so we need to remove those from the
    # query set. Using distinct() in this case will not remove the
    # duplicate model instances. See note at:
    # https://docs.djangoproject.com/en/5.0/ref/models/querysets/#django.db.models.query.QuerySet.distinct
    unique_albums = list(OrderedDict.fromkeys(albums))

    return 200, unique_albums


@api.get("albums/{int:id}/discs/")
def retrieve_album_discs(request, id: int):
    pass


@api.get("albums/{int:id}/songs/")
def retrieve_album_songs(request, id: int):
    pass
