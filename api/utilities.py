from typing import Any


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
