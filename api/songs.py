from django import db
from ninja import Router

from catalog import models
from api import schema, utilities as util

router = Router()


@router.post("", response={201: schema.SongOut, 400: schema.Error, 404: schema.Error}, tags=["songs"])
def create_song(request, data: schema.SongIn):
    data = util.strip_whitespace(data.dict())
    try:
        data["album"] = models.Album.objects.get(pk=data["album"])
        if data["disc"]:
            data["disc"] = models.Disc.objects.get(pk=data["disc"])
        song = models.Song.objects.create(**data)
    except models.Album.DoesNotExist:
        return 404, {"error": f"Album with id = {data["album"]} does not exist."}
    except models.Disc.DoesNotExist:
        return 404, {"error": f"Disc with id = {data["disc"]} does not exist."}
    except db.IntegrityError:
        return 400, {"error": "Song already exists in database."}
    else:
        return 201, song


@router.get(
    "{int:id}",
    response={200: schema.SongOut, 404: schema.Error},
    tags=["songs"],
)
def retrieve_song(request, id: int):
    try:
        song = models.Song.objects.get(pk=id)
    except models.Song.DoesNotExist:
        return 404, {"error": f"Song with id = {id} does not exist."}
    else:
        return 200, song


@router.put(
    "{int:id}",
    response={200: schema.SongOut, 404: schema.Error},
    tags=["songs"],
)
def update_song(request, id: int, data: schema.SongIn):
    data = util.strip_whitespace(data.dict())
    try:
        song = models.Song.objects.get(pk=id)
        data["album"] = models.Album.objects.get(pk=data["album"])
        if data["disc"]:
            data["disc"] = models.Disc.objects.get(pk=data["disc"])
    except models.Song.DoesNotExist:
        return 404, {"error": f"Song with id = {id} does not exist."}
    except models.Album.DoesNotExist:
        return 404, {"error": f"Album with id = {data["album"]} does not exist."}
    except models.Disc.DoesNotExist:
        return 404, {"error": f"Disc with id = {data["disc"]} does not exist."}
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
    response={201: schema.FeatureOut, 400: schema.Error, 404: schema.Error},
    tags=["songs"],
)
def create_song_feature(request, id: int, data: schema.FeatureIn):
    data = util.strip_whitespace(data.dict())
    try:
        data["song"] = models.Song.objects.get(pk=id)
        data["artist"] = models.Artist.objects.get(pk=data["artist"])
        feature = models.Feature.objects.create(**data)
    except models.Song.DoesNotExist:
        return 404, {"error": f"Song with id = {id} does not exist."}
    except models.Artist.DoesNotExist:
        return 404, {"error": f"Artist with id = {data["artist"]} does not exist."}
    except db.IntegrityError as error:
        error = str(error.__cause__)
        if "check constraint" in error:
            message = ("There is something wrong with the data submitted. "
                       "Please consult the API documentation and try again.")
            return 400, {"error": message}
        elif "unique constraint" in error:
            if data["producer"]:
                message = (f"Artist with id = {data["artist"].id} is already "
                           f"credited as a producer for song with id = {id}.")
            else:
                message = (f"Artist with id = {data["artist"].id} is already "
                           f"credited as a song artist for song with id = {id}.")
            return 400, {"error": message}
        else:
            return 400, {"error": error}
    else:
        return 201, feature
