from typing import List

from ninja import NinjaAPI

from catalog import models, schema
from catalog import utilities as util

api = NinjaAPI(version="1.0")


@api.post("artists/", response={201: schema.DetailedArtistOut}, tags=["artists"])
def create_artist(request, data: schema.ArtistIn):
    data = util.strip_whitespace(data.dict())
    artist = models.Artist.objects.create(**data)
    artist.request = request
    return artist


@api.get(
    "artists/{int:id}",
    response={200: schema.DetailedArtistOut, 404: schema.Error},
    tags=["artists"],
)
def retrieve_artist(request, id: int):
    try:
        artist = models.Artist.objects.get(pk=id)
        artist.request = request
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
        artist.request = request
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
