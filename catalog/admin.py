from django.contrib import admin

from catalog import models

admin.site.register(models.Artist)
admin.site.register(models.Album)
admin.site.register(models.Disc)
admin.site.register(models.Song)
admin.site.register(models.Feature)
admin.site.register(models.Playlist)
admin.site.register(models.PlaylistSong)
admin.site.register(models.Hub)
