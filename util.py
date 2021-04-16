def calculate_names_length(*args, **kwargs):
    length = 0
    for name in args:
        length += len(name.replace(' ', '').replace('-', ''))

    return length
