from django import db
from ninja import Router

from catalog import models
from api import schema, utilities as util

router = Router()


@router.post("", response={201: schema.SongOut, 404: schema.Error}, tags=["songs"])
def create_song(request, data: schema.SongIn):
    data = util.strip_whitespace(data.dict())
    data["album"] = models.Album.objects.get(pk=data["album"])
    if data["disc"]:
        data["disc"] = models.Disc.objects.get(pk=data["disc"])

    try:
        song = models.Song.objects.create(**data)
    except db.IntegrityError:
        return 404, {"error": "Song already exists in database."}
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
        return 200, song
    except models.Song.DoesNotExist:
        return 404, {"error": f"Song with id = {id} does not exist."}


@router.put(
    "{int:id}",
    response={200: schema.SongOut, 404: schema.Error},
    tags=["songs"],
)
def update_song(request, id: int, data: schema.SongIn):
    try:
        song = models.Song.objects.get(pk=id)
        data = util.strip_whitespace(data.dict())
        data["album"] = models.Album.objects.get(pk=data["album"])
        if data["disc"]:
            data["disc"] = models.Disc.objects.get(pk=data["disc"])
        for attr, value in data.items():
            setattr(song, attr, value)
        song.save()
        return 200, song
    except models.Song.DoesNotExist:
        return 404, {"error": f"Song with id = {id} does not exist."}


@router.delete("{int:id}", response={204: None, 404: schema.Error}, tags=["songs"])
def delete_song(request, id: int):
    try:
        song = models.Song.objects.get(pk=id)
        song.delete()
        return 204, None
    except models.Song.DoesNotExist:
        return 404, {"error": f"Song with id = {id} does not exist."}
