import string


def strip_whitespace(data: dict) -> dict:
    """Remove extraneous whitespace from string values in dictionary
    passed as data.
    """
    for key, value in data.items():
        if isinstance(value, str):
            value = value.strip()
            while "  " in value:  # Remove extraneous whitespace between words.
                value = value.replace("  ", " ")
            data[key] = value

    return data


def normalize_text(text: str) -> str:
    """Remove punctuation and capitalization from string passed as text."""
    replacements = {
        "+": "and",
        "&": "and",
        "#": "number",
        "=": "equal",
    }

    for mark in list(string.punctuation):
        if mark in replacements.keys():
            text = text.replace(mark, replacements[mark])
        else:
            text = text.replace(mark, "")

    return text.lower()
