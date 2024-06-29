from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="catalog/", permanent=True)),
    path("admin/", admin.site.urls),
]
