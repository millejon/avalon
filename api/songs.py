from django.db import IntegrityError
from ninja import Router

from api import models
from api import schema, utilities as util

router = Router()


@router.post("", response={201: schema.SongOut, 400: schema.Error, 404: schema.Error}, tags=["songs"])
def create_song(request, data: schema.SongIn):
    data = util.strip_whitespace(data.dict())
    try:
        data["album"] = models.Album.objects.get(pk=data["album"])
        song = models.Song.objects.create(**data)
    except models.Album.DoesNotExist:
        return 404, {"error": f"Album with id = {data["album"]} does not exist."}
    except IntegrityError as error:
        error = str(error.__cause__)
        if "check constraint" in error:
            message = ("There is something wrong with the data submitted. "
                       "Please consult the API documentation and try again.")
            return 400, {"error": message}
        elif "unique constraint" in error:
            return 400, {"error": "Song already exists in database."}
        else:
            return 400, {"error": error}
    else:
        return 201, song


@router.get("{int:id}", response={200: schema.SongOut, 404: schema.Error}, tags=["songs"])
def retrieve_song(request, id: int):
    try:
        song = models.Song.objects.get(pk=id)
    except models.Song.DoesNotExist:
        return 404, {"error": f"Song with id = {id} does not exist."}
    else:
        return 200, song


@router.put("{int:id}", response={200: schema.SongOut, 404: schema.Error}, tags=["songs"])
def update_song(request, id: int, data: schema.SongIn):
    data = util.strip_whitespace(data.dict())
    try:
        song = models.Song.objects.get(pk=id)
        data["album"] = models.Album.objects.get(pk=data["album"])
    except models.Song.DoesNotExist:
        return 404, {"error": f"Song with id = {id} does not exist."}
    except models.Album.DoesNotExist:
        return 404, {"error": f"Album with id = {data["album"]} does not exist."}
    else:
        for attr, value in data.items():
            setattr(song, attr, value)
        song.save()
        return 200, song


@router.delete("{int:id}", response={204: None, 404: schema.Error}, tags=["songs"])
def delete_song(request, id: int):
    try:
        song = models.Song.objects.get(pk=id)
    except models.Song.DoesNotExist:
        return 404, {"error": f"Song with id = {id} does not exist."}
    else:
        song.delete()
        return 204, None


@router.post(
    "{int:id}/artists",
    response={201: schema.SongArtistOut, 400: schema.Error, 404: schema.Error},
    tags=["songs"],
)
def create_song_artist(request, id: int, data: schema.SongArtistIn):
    data = data.dict()
    try:
        data["song"] = models.Song.objects.get(pk=id)
        data["artist"] = models.Artist.objects.get(pk=data["artist"])
        song_artist = models.SongArtist.objects.create(**data)
    except models.Song.DoesNotExist:
        return 404, {"error": f"Song with id = {id} does not exist."}
    except models.Artist.DoesNotExist:
        return 404, {"error": f"Artist with id = {data["artist"]} does not exist."}
    except IntegrityError as error:
        error = str(error.__cause__)
        if "unique constraint" in error:
            message = (f"Artist with id = {data["artist"].id} is already "
                       f"credited as an artist for song with id = {id}.")
            return 400, {"error": message}
        else:
            return 400, {"error": error}
    else:
        return 201, song_artist


@router.get(
    "{int:id}/artists",
    response={200: schema.SongArtistsOut, 404: schema.Error},
    tags=["songs"],
)
def retrieve_all_song_artists(request, id: int):
    try:
        song = models.Song.objects.get(pk=id)
    except models.Song.DoesNotExist:
        return 404, {"error": f"Song with id = {id} does not exist."}
    else:
        return 200, song


@router.delete(
    "{int:song_id}/artists/{int:artist_id}",
    response={204: None, 404: schema.Error},
    tags=["songs"],
)
def delete_song_artist(request, song_id: int, artist_id: int):
    try:
        song = models.Song.objects.get(pk=song_id)
        artist = models.Artist.objects.get(pk=artist_id)
    except models.Song.DoesNotExist:
        return 404, {"error": f"Song with id = {song_id} does not exist."}
    except models.Artist.DoesNotExist:
        return 404, {"error": f"Artist with id = {artist_id} does not exist."}
    else:
        song.artists.remove(artist)
        return 204, None


@router.post(
    "{int:id}/producers",
    response={201: schema.SongProducerOut, 400: schema.Error, 404: schema.Error},
    tags=["songs"],
)
def create_song_producer(request, id: int, data: schema.SongProducerIn):
    data = util.strip_whitespace(data.dict())
    try:
        data["song"] = models.Song.objects.get(pk=id)
        data["producer"] = models.Artist.objects.get(pk=data["producer"])
        song_producer = models.SongProducer.objects.create(**data)
    except models.Song.DoesNotExist:
        return 404, {"error": f"Song with id = {id} does not exist."}
    except models.Artist.DoesNotExist:
        return 404, {"error": f"Artist with id = {data["producer"]} does not exist."}
    except IntegrityError as error:
        error = str(error.__cause__)
        if "unique constraint" in error:
            message = (f"Artist with id = {data["producer"].id} is already "
                       f"credited as a producer for song with id = {id}.")
            return 400, {"error": message}
        else:
            return 400, {"error": error}
    else:
        return 201, song_producer


@router.get(
    "{int:id}/producers",
    response={200: schema.SongProducersOut, 404: schema.Error},
    tags=["songs"],
)
def retrieve_all_song_producers(request, id: int):
    try:
        song = models.Song.objects.get(pk=id)
    except models.Song.DoesNotExist:
        return 404, {"error": f"Song with id = {id} does not exist."}
    else:
        return 200, song


@router.delete(
    "{int:song_id}/producers/{int:producer_id}",
    response={204: None, 404: schema.Error},
    tags=["songs"],
)
def delete_song_producer(request, song_id: int, producer_id: int):
    try:
        song = models.Song.objects.get(pk=song_id)
        producer = models.Artist.objects.get(pk=producer_id)
    except models.Song.DoesNotExist:
        return 404, {"error": f"Song with id = {song_id} does not exist."}
    except models.Artist.DoesNotExist:
        return 404, {"error": f"Artist with id = {producer_id} does not exist."}
    else:
        song.producers.remove(producer)
        return 204, None
