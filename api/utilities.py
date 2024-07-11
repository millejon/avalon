def strip_whitespace(data):
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.strip()
    return data
