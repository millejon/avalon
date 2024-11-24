from django.db import IntegrityError
from ninja import Router

from api import models
from api import schema, utilities as util

router = Router()


@router.post("", response={201: schema.ArtistOut, 400: schema.Error})
def create_artist(request, data: schema.ArtistIn):
    """To create an artist, include the following fields in the request
    body:
    - **name** (*string*): The name of the artist or group (e.g.,
    "Jay-Z") ***required***
    - **hometown** (*string*): The city the artist is most associated
    with (e.g., "New York, NY") ***optional***
    """
    artist_data = util.strip_whitespace(data.dict())
    try:
        artist = models.Artist.objects.create(**artist_data)
    except IntegrityError as error:
        error = str(error.__cause__)
        if "unique constraint" in error:
            return 400, {"error": "Artist already exists in database."}
        else:
            return 400, {"error": error}
    else:
        return 201, artist


@router.get("{int:id}")
def retrieve_artist(request, id: int):
    pass


@router.get("{int:id}/albums")
def retrieve_artist_albums(request, id: int):
    pass


@router.get("{int:id}/singles")
def retrieve_artist_singles(request, id: int):
    pass
