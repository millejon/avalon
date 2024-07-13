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


@router.get("{int:id}")
def retrieve_disc(request, id: int):
    pass
