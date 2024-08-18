from typing import List

from ninja import Router

from api import models
from api import schema, utilities as util

router = Router()


@router.post("", response={201: schema.Artist}, tags=["artists"])
def create_artist(request, data: schema.ArtistIn):
    data = util.strip_whitespace(data.dict())
    artist = models.Artist.objects.create(**data)
    return 201, artist


@router.get(
    "{int:id}",
    response={200: schema.Artist, 404: schema.Error},
    tags=["artists"],
)
def retrieve_artist(request, id: int):
    try:
        artist = models.Artist.objects.get(pk=id)
        return 200, artist
    except models.Artist.DoesNotExist:
        return 404, {"error": f"Artist with id = {id} does not exist."}


@router.put(
    "{int:id}",
    response={200: schema.Artist, 404: schema.Error},
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


@router.delete("{int:id}", response={204: None, 404: schema.Error}, tags=["artists"])
def delete_artist(request, id: int):
    try:
        artist = models.Artist.objects.get(pk=id)
        artist.delete()
        return 204, None
    except models.Artist.DoesNotExist:
        return 404, {"error": f"Artist with id = {id} does not exist."}


# TODO: Write tests for this endpoint after finishing album endpoints
@router.get("", response={200: List[schema.ArtistBasics]}, tags=["artists"])
def retrieve_all_artists(request):
    artists = models.Artist.objects.filter(album__isnull=False).distinct("name")
    return 200, artists


@router.get("{int:id}/albums")
def retrieve_artist_albums(request, id: int):
    pass


@router.get("{int:id}/singles")
def retrieve_artist_singles(request, id: int):
    pass


@router.get("{int:id}/songs")
def retrieve_artist_songs(request, id: int):
    pass


@router.get("{int:id}/produced")
def retrieve_artist_production_credits(request, id: int):
    pass
