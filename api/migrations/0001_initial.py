# Generated by Django 5.0.6 on 2024-06-16 17:43

import django.core.validators
import django.db.models.deletion
import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name="Album",
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
                ("release_date", models.DateField()),
                ("single", models.BooleanField(blank=True, default=False)),
                ("multidisc", models.BooleanField(blank=True, default=False)),
            ],
            options={
                "ordering": ["artists__name", "release_date"],
            },
        ),
        migrations.CreateModel(
            name="Artist",
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
                ("name", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Disc",
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
                ("title", models.CharField(max_length=100)),
                (
                    "number",
                    models.PositiveSmallIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
            ],
            options={
                "ordering": ["album__artists__name", "album__release_date", "number"],
            },
        ),
        migrations.CreateModel(
            name="Feature",
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
                ("producer", models.BooleanField(blank=True, default=False)),
                ("role", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Hub",
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
                ("name", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Playlist",
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
                ("title", models.CharField(max_length=300, unique=True)),
            ],
            options={
                "ordering": [
                    "songs__album__release_date",
                    "songs__disc__number",
                    "songs__track_number",
                ],
            },
        ),
        migrations.CreateModel(
            name="PlaylistSong",
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
                ("date_added", models.DateTimeField(auto_now_add=True)),
            ],
        ),
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
                    "track_number",
                    models.PositiveSmallIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                ("length", models.PositiveIntegerField()),
                ("play_count", models.PositiveIntegerField(default=0)),
                ("path", models.CharField(max_length=300, unique=True)),
            ],
            options={
                "ordering": ["-album__release_date", "disc__number", "track_number"],
            },
        ),
        migrations.AddConstraint(
            model_name="artist",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("name"),
                name="artist_name_case_insensitive_unique",
                violation_error_message="Artist already exists (case insensitive match)",
            ),
        ),
        migrations.AddField(
            model_name="album",
            name="artists",
            field=models.ManyToManyField(to="api.artist"),
        ),
        migrations.AddField(
            model_name="disc",
            name="album",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.album"
            ),
        ),
        migrations.AddField(
            model_name="feature",
            name="artist",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.artist"
            ),
        ),
        migrations.AddField(
            model_name="hub",
            name="albums",
            field=models.ManyToManyField(blank=True, to="api.album"),
        ),
        migrations.AddField(
            model_name="hub",
            name="artists",
            field=models.ManyToManyField(blank=True, to="api.artist"),
        ),
        migrations.AddField(
            model_name="playlistsong",
            name="playlist",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.playlist"
            ),
        ),
        migrations.AddField(
            model_name="song",
            name="album",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.album"
            ),
        ),
        migrations.AddField(
            model_name="song",
            name="artists",
            field=models.ManyToManyField(through="api.Feature", to="api.artist"),
        ),
        migrations.AddField(
            model_name="song",
            name="disc",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="api.disc",
            ),
        ),
        migrations.AddField(
            model_name="playlistsong",
            name="song",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.song"
            ),
        ),
        migrations.AddField(
            model_name="playlist",
            name="songs",
            field=models.ManyToManyField(
                blank=True, through="api.PlaylistSong", to="api.song"
            ),
        ),
        migrations.AddField(
            model_name="feature",
            name="song",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.song"
            ),
        ),
        migrations.AddConstraint(
            model_name="album",
            constraint=models.UniqueConstraint(
                fields=("title", "release_date"), name="unique_album"
            ),
        ),
        migrations.AddConstraint(
            model_name="disc",
            constraint=models.UniqueConstraint(
                fields=("album", "number"), name="unique_disc"
            ),
        ),
        migrations.AddConstraint(
            model_name="hub",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("name"),
                name="hub_name_case_insensitive_unique",
                violation_error_message="Hub already exists (case insensitive match)",
            ),
        ),
        migrations.AddConstraint(
            model_name="playlist",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("title"),
                name="playlist_title_case_insensitive_unique",
                violation_error_message="Playlist already exists (case insensitive match)",
            ),
        ),
        migrations.AddConstraint(
            model_name="feature",
            constraint=models.UniqueConstraint(
                fields=("artist", "song", "group"), name="unique_vocalist"
            ),
        ),
        migrations.AddConstraint(
            model_name="feature",
            constraint=models.UniqueConstraint(
                fields=("artist", "song", "producer"), name="unique_producer"
            ),
        ),
    ]
