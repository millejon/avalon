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


@api.get("artists/{int:id}", tags=["artists"])
def retrieve_artist(request, id: int):
    pass


@api.get("artists/{int:id}/albums/", tags=["artists"])
def retrieve_artist_albums(request, id: int):
    pass


@api.get("artists/{int:id}/singles/", tags=["artists"])
def retrieve_artist_singles(request, id: int):
    pass


@api.get("artists/{int:id}/songs/", tags=["artists"])
def retrieve_artist_songs(request, id: int):
    pass


@api.get("artists/{int:id}/produced/", tags=["artists"])
def retrieve_artist_production_credits(request, id: int):
    pass
