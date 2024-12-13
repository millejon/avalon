from ninja import NinjaAPI
from api.artists import router as artists_router
from api.albums import router as albums_router

api = NinjaAPI(urls_namespace="api")

api.add_router("artists/", artists_router, tags=["artists"])
api.add_router("albums/", albums_router, tags=["albums"])
