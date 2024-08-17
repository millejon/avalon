from collections import OrderedDict
from typing import List

from django.db import IntegrityError
from ninja import Router

from api import models
from api import schema, utilities as util

router = Router()


@router.post("", response={201: schema.AlbumOut, 400: schema.Error}, tags=["albums"])
def create_album(request, data: schema.AlbumIn):
    data = util.strip_whitespace(data.dict())
    try:
        album = models.Album.objects.create(**data)
    except IntegrityError as error:
        error = str(error.__cause__)
        if "unique constraint" in error:
            return 400, {"error": "Album already exists in database."}
        elif "check constraint" in error:
            return 400, {"error": "Singles can not be multidisc."}
        else:
            return 400, {"error": error}
    else:
        return 201, album


@router.get(
    "{int:id}", response={200: schema.AlbumOut, 404: schema.Error}, tags=["albums"]
)
def retrieve_album(request, id: int):
    try:
        album = models.Album.objects.get(pk=id)
    except models.Album.DoesNotExist:
        return 404, {"error": f"Album with id = {id} does not exist."}
    else:
        return 200, album


@router.put(
    "{int:id}", response={200: schema.AlbumOut, 404: schema.Error}, tags=["albums"]
)
def update_album(request, id: int, data: schema.AlbumIn):
    data = util.strip_whitespace(data.dict())
    try:
        album = models.Album.objects.get(pk=id)
    except models.Album.DoesNotExist:
        return 404, {"error": f"Album with id = {id} does not exist."}
    else:
        for attr, value in data.items():
            setattr(album, attr, value)
        album.save()
        return 200, album


@router.delete("{int:id}", response={204: None, 404: schema.Error}, tags=["albums"])
def delete_album(request, id: int):
    try:
        album = models.Album.objects.get(pk=id)
    except models.Album.DoesNotExist:
        return 404, {"error": f"Album with id = {id} does not exist."}
    else:
        album.delete()
        return 204, None


# TODO: Need to figure out how to order albums by first artist added to
# TODO: album, not just first alphabetical album artist, then write
# TODO: tests for this endpoint.
@router.get("", response={200: List[schema.AlbumSummaryOut]}, tags=["albums"])
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


@router.get("{int:id}/discs")
def retrieve_album_discs(request, id: int):
    pass


@router.get("{int:id}/songs")
def retrieve_album_songs(request, id: int):
    pass
