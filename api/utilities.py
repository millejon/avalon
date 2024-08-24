def strip_whitespace(data: dict) -> dict:
    """Remove extraneous whitespace from string values in dictionary
    passed as data.
    """
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.strip()

    return data
