from ninja import NinjaAPI
from api.artists import router as artists_router
from api.albums import router as albums_router
from api.discs import router as discs_router

api = NinjaAPI(version="1.0")

api.add_router("artists/", artists_router)
api.add_router("albums/", albums_router)
api.add_router("discs/", discs_router)
