from django.http import HttpResponse


def index(request):
    return HttpResponse("To use this API, please refer to the documentation.")
