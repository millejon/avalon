from django.contrib import admin

from api import models

admin.site.register(models.Artist)
admin.site.register(models.Album)
admin.site.register(models.AlbumArtist)
admin.site.register(models.Song)
admin.site.register(models.SongArtist)
admin.site.register(models.SongProducer)
