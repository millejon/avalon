from ninja import Router

from catalog import models
from api import schema, utilities as util

router = Router()


@router.post("", response={201: schema.SongOut}, tags=["songs"])
def create_song(request, data: schema.SongIn):
    data = util.strip_whitespace(data.dict())
    data["album"] = models.Album.objects.get(pk=data["album"])
    if data["disc"]:
        data["disc"] = models.Disc.objects.get(pk=data["disc"])
    song = models.Song.objects.create(**data)
    return 201, song


@router.get(
    "{int:id}",
    response={200: schema.SongOut, 404: schema.Error},
    tags=["songs"],
)
def retrieve_song(request, id: int):
    pass
