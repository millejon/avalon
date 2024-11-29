# Generated by Django 5.1.3 on 2024-11-29 22:59

import django.core.validators
import django.db.models.deletion
import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_alter_album_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Song",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=600)),
                (
                    "disc",
                    models.PositiveSmallIntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
                (
                    "track_number",
                    models.PositiveSmallIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                ("length", models.PositiveSmallIntegerField()),
                ("path", models.CharField(max_length=1000, unique=True)),
                ("play_count", models.PositiveIntegerField(default=0)),
                (
                    "album",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.album"
                    ),
                ),
            ],
            options={
                "ordering": [
                    "-play_count",
                    "-album__release_date",
                    "disc",
                    "track_number",
                ],
            },
        ),
        migrations.CreateModel(
            name="SongArtist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("group", models.BooleanField(blank=True, default=False)),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.artist"
                    ),
                ),
                (
                    "song",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.song"
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
        ),
        migrations.AddField(
            model_name="song",
            name="artists",
            field=models.ManyToManyField(
                related_name="song_artists", through="api.SongArtist", to="api.artist"
            ),
        ),
        migrations.CreateModel(
            name="SongProducer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("role", models.CharField(max_length=100)),
                (
                    "producer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.artist"
                    ),
                ),
                (
                    "song",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.song"
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
        ),
        migrations.AddField(
            model_name="song",
            name="producers",
            field=models.ManyToManyField(
                related_name="song_producers",
                through="api.SongProducer",
                to="api.artist",
            ),
        ),
        migrations.AddConstraint(
            model_name="songartist",
            constraint=models.UniqueConstraint(
                fields=("song", "artist"), name="duplicate_song_artist"
            ),
        ),
        migrations.AddConstraint(
            model_name="songproducer",
            constraint=models.UniqueConstraint(
                fields=("song", "producer"), name="duplicate_producer"
            ),
        ),
        migrations.AddConstraint(
            model_name="song",
            constraint=models.UniqueConstraint(
                fields=("album", "disc", "track_number"), name="duplicate_track_number"
            ),
        ),
        migrations.AddConstraint(
            model_name="song",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("path"),
                name="duplicate_song_case_insensitive_match",
            ),
        ),
        migrations.AddConstraint(
            model_name="song",
            constraint=models.CheckConstraint(
                condition=models.Q(("disc__gte", 1)),
                name="disc_number_must_be_greater_than_0",
            ),
        ),
        migrations.AddConstraint(
            model_name="song",
            constraint=models.CheckConstraint(
                condition=models.Q(("track_number__gte", 1)),
                name="track_number_must_be_greater_than_0",
            ),
        ),
    ]