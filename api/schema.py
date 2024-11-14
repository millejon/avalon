from ninja import Schema


class ArtistIn(Schema):
    name: str
    hometown: str = ""


class ArtistOut(Schema):
    id: int
    name: str
    hometown: str | None
    url: str

    @staticmethod
    def resolve_hometown(obj):
        return obj.hometown if obj.hometown else None

    @staticmethod
    def resolve_url(obj, context):
        return context["request"].build_absolute_uri(obj.get_url())
