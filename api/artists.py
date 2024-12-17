from django.db import IntegrityError
from ninja import Router
from ninja.responses import codes_4xx

from api import models, schema, utilities as util

router = Router()


@router.post("", response={201: schema.ArtistOut, codes_4xx: schema.Error})
def create_artist(request, data: schema.ArtistIn):
    """To create an artist, include the following fields in the request
    body:
    - **name** (*string*): The name of the artist or group (e.g., "The
    Notorious B.I.G.") ***required***
    - **hometown** (*string*): The city the artist is most associated
    with (e.g., "New York, NY") ***optional***
    """
    artist_data = util.strip_whitespace(data.dict())

    try:
        artist = models.Artist.objects.create(**artist_data)

    except IntegrityError as error:
        error = str(error.__cause__)
        if "unique constraint" in error:
            return 409, {"error": "Artist already exists in database."}
        else:
            return 400, {"error": error}

    else:
        return 201, artist


@router.get("{int:id}", response={200: schema.ArtistOut, codes_4xx: schema.Error})
def retrieve_artist(request, id: int):
    try:
        artist = models.Artist.objects.get(pk=id)

    except models.Artist.DoesNotExist:
        return 404, {"error": f"Artist with id = {id} does not exist."}

    else:
        return artist


@router.get("{int:id}/albums")
def retrieve_artist_albums(request, id: int):
    pass


@router.get("{int:id}/singles")
def retrieve_artist_singles(request, id: int):
    pass


@router.get("{int:id}/songs")
def retrieve_artist_songs(request, id: int):
    pass


@router.get("{int:id}/songs-produced")
def retrieve_artist_songs_produced(request, id: int):
    pass
