from django.db import IntegrityError
from ninja import Router

from api import models, schema, utilities as util

router = Router()


@router.post("", response={201: schema.AlbumOut, 400: schema.Error})
def create_album(request, data: schema.AlbumIn):
    """To create an album, include the following fields in the request
    body:
    - **title** (*string*): The title of the album (e.g., "Reasonable
    Doubt") ***required***
    - **artists** (*list[dict]*): The artists attributed to the album
    ***required***\\
        Each artist is an object with the following fields:
        - **name** (*string*): The name of the artist or group (e.g.,
        "Jay-Z") ***required***
        - **hometown** (*string*): The city the artist is most
        associated with (e.g., "New York, NY") ***optional***
    - **release_date** (*date*): The release date of the album in
    YYYY-MM-DD format (e.g., "1996-06-25") ***required***
    - **label** (*string*): The record label that released the album
    (e.g. "Roc-A-Fella Records") ***optional***
    - **album_type** (*string*): This must be either "album",
    "multidisc", or "single", defaults to "album" ***optional***
    """
    album_data = util.strip_whitespace(data.dict())
    artist_data = album_data.pop("artists")
    try:
        album = models.Album.objects.create(**album_data)
    except IntegrityError as error:
        error = str(error.__cause__)
        if "unique constraint" in error:
            return 400, {"error": "Album already exists in database."}
        else:
            return 400, {"error": error}
    else:
        album.artists.set(util.get_artists(artist_data))
        return 201, album


@router.get("{int:id}")
def retrieve_album(request, id: int):
    pass


@router.get("{int:id}/songs")
def retrieve_album_songs(request, id: int):
    pass
