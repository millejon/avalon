from django.db import IntegrityError
from ninja import Router
from ninja.responses import codes_4xx

from api import models, schema, utilities as util

router = Router()


@router.post("", response={201: schema.AlbumOut, codes_4xx: schema.Error})
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
            return 409, {"error": "Album already exists in database."}
        else:
            return 400, {"error": error}

    else:
        album.artists.set(util.get_artists(artist_data))

        return 201, album


@router.post(
    "{int:id}/songs",
    response={201: schema.SongOut, codes_4xx: schema.Error},
    tags=["songs"],
)
def create_song(request, id: int, data: schema.SongIn):
    """To create a song, include the following fields in the request
    body:
    - **title** (*string*): The title of the song (e.g., "Protect Ya
    Neck") ***required***
    - **artists** (*list[dict]*): The artists featured on the song
    ***required***
    - **group_members** (*list[dict]*): The group affiliations of the
    song artists, can be either the individual group members featured
    on the song if the main song artist is a group or the group if the
    main song artists include multiple members of a group ***optional***
    - **producers** (*list[dict]*): The producers of the song
    ***optional***\\
        Each artist, group member, and producer is an object with the
        following fields:
        - **name** (*string*): The name of the artist or group (e.g.,
        "RZA") ***required***
        - **hometown** (*string*): The city the artist is most
        associated with (e.g., "New York, NY") ***optional***
    - **disc** (*integer*): The disc of the album that the song is on,
    defaults to 1 ***optional***
    - **track_number** (*integer*): The position of the song in the
    tracklist of the album (e.g. 10) ***required***
    - **length** (*integer*): The length of the song in seconds (e.g. 292)
    ***required***
    - **path** (*string*): The file path of the local music file for the
    song (e.g. "/wutang-clan/enter-the-wutang-36-chambers/10_protect_ya_neck.flac")
    ***required***
    """
    song_data = util.strip_whitespace(data.dict())
    artist_data = song_data.pop("artists")
    group_member_data = song_data.pop("group_members")
    producer_data = song_data.pop("producers")

    try:
        song_data["album"] = models.Album.objects.get(pk=id)
        song = models.Song.objects.create(**song_data)

    except models.Album.DoesNotExist:
        return 404, {"error": f"Album with id = {id} does not exist."}
    except IntegrityError as error:
        error = str(error.__cause__)
        if "duplicate_track_number" in error:
            return 409, {
                "error": f"Album already has a song with track number = {song_data["track_number"]}."
            }
        elif "unique constraint" in error:
            return 409, {"error": "Song already exists in database."}
        elif "disc_number_must_be_greater_than_0" in error:
            return 400, {"error": "Disc must be a positive integer greater than 0."}
        elif "track_number_must_be_greater_than_0" in error:
            return 400, {
                "error": "Track number must be a positive integer greater than 0."
            }
        else:
            return 400, {"error": error}

    else:
        song.artists.set(util.get_artists(artist_data))
        if group_member_data:
            song.artists.add(
                *util.get_artists(group_member_data), through_defaults={"group": True}
            )
        if producer_data:
            song.producers.set(util.get_artists(producer_data))

        return 201, song


@router.get("{int:id}")
def retrieve_album(request, id: int):
    pass


@router.get("{int:id}/songs")
def retrieve_album_songs(request, id: int):
    pass
