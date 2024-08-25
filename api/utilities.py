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
