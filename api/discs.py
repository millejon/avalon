from ninja import Router

from catalog import models
from api import schema, utilities as util

router = Router()


@router.post("", response={201: schema.DiscOut}, tags=["discs"])
def create_disc(request, data: schema.DiscIn):
    data = util.strip_whitespace(data.dict())
    data["album"] = models.Album.objects.get(pk=data["album"])
    disc = models.Disc.objects.create(**data)
    return 201, disc


@router.get(
    "{int:id}", response={200: schema.DiscOut, 404: schema.Error}, tags=["discs"]
)
def retrieve_disc(request, id: int):
    try:
        disc = models.Disc.objects.get(pk=id)
        return 200, disc
    except models.Disc.DoesNotExist:
        return 404, {"error": f"Disc with id = {id} does not exist."}


@router.get("{int:id}/songs/")
def retrieve_disc_songs(request, id: int):
    pass
