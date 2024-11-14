from ninja import NinjaAPI
from api.artists import router as artists_router

api = NinjaAPI(urls_namespace="api")

api.add_router("artists/", artists_router, tags=["artists"])
