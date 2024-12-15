# from django.db import IntegrityError
from ninja import Router

# from api import models, schema, utilities as util

router = Router()


@router.get("{int:id}")
def retrieve_song(request, id: int):
    pass
