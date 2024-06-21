from django.http import HttpResponse


def index(request):
    return HttpResponse(
        "Hello, world! A journey of a thousand miles begins with a single step."
    )
