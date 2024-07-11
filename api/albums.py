from collections import OrderedDict
from typing import List

from ninja import Router

from catalog import models
from api import schema, utilities as util

router = Router()


@router.post("", response={201: schema.DetailedAlbumOut}, tags=["albums"])
def create_album(request, data: schema.AlbumIn):
    data = util.strip_whitespace(data.dict())
    artists = data.pop("artists")

    album = models.Album.objects.create(**data)
    for artist in artists:
        album.artists.add(artist)
    album.save()
    return 201, album


@router.get(
    "{int:id}",
    response={200: schema.DetailedAlbumOut, 404: schema.Error},
    tags=["albums"],
)
def retrieve_album(request, id: int):
    try:
        album = models.Album.objects.get(pk=id)
        return 200, album
    except models.Album.DoesNotExist:
        return 404, {"error": f"Album with id = {id} does not exist."}


@router.put(
    "{int:id}",
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


@router.delete("{int:id}", response={204: None, 404: schema.Error}, tags=["albums"])
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
@router.get("", response={200: List[schema.AlbumOut]}, tags=["albums"])
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


@router.get("{int:id}/discs/")
def retrieve_album_discs(request, id: int):
    pass


@router.get("{int:id}/songs/")
def retrieve_album_songs(request, id: int):
    pass
