from typing import Any

from api import models


def get_artists(artist_data: list[dict[str, str]]) -> list[models.Artist]:
    """Retrieve Artist objects from the database.

    This utility accepts a list of dictionaries containing artist
    metadata. For each artist in the list, the corresponding Artist
    object will be retrieved from the database. If the artist does not
    yet exist in the database, then a new Artist object will be created.
    If the artist metadata has a value for the hometown attribute while
    the corresponding Artist object does not, then the Artist object
    will be updated accordingly.

    Arguments:
        artist_data (list) -- A list of dictionaries where each
        dictionary contains the metadata for one artist. Each dictionary
        should have the following fields:
            name (str) - The name of the artist or group (e.g. "Jay-Z")
            [required]
            hometown (str) - The city the artist is most associated with
            (e.g. "New York, NY") [optional]

    Returns:
        artists (list) -- A list of Artist objects.
    """
    artists = []

    for data in artist_data:
        data = strip_whitespace(data)
        try:
            artist = models.Artist.objects.get(name__iexact=data["name"])
        except models.Artist.DoesNotExist:
            artist = models.Artist.objects.create(**data)
        finally:
            if data["hometown"] and artist.hometown != data["hometown"]:
                artist.hometown = data["hometown"]
                artist.save()
            artists.append(artist)

    return artists


def strip_whitespace(data: dict[Any, Any]) -> dict[Any, Any]:
    """Remove extraneous whitespace from string values in a dictionary.

    This utility will strip whitespace from the beginning and end of
    all string values in a dictionary. If the string has multiple spaces
    between words, then those will be stripped as well so only one space
    remains. All non-string fields of the dictionary will be ignored.

    Arguments:
        data (dict) -- A dictionary that may contain string values with
        extraneous whitespace.

    Returns:
        data (dict) -- A dictionary with all extraneous whitespace
        removed from its string values.
    """
    for key, value in data.items():
        if isinstance(value, str):
            value = value.strip()
            while "  " in value:  # Remove extraneous whitespace between words.
                value = value.replace("  ", " ")
            data[key] = value

    return data
