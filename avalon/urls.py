from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from catalog.api import api

urlpatterns = [
    path("", RedirectView.as_view(url="catalog/", permanent=True)),
    path("api/v1/", api.urls),
    path("admin/", admin.site.urls),
]
