# Generated by Django 5.1.3 on 2024-11-30 23:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_song_songartist_song_artists_songproducer_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="songproducer",
            name="role",
        ),
    ]
