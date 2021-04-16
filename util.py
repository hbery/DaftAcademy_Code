import re

def calculate_names_length(*args, **kwargs):
    length = 0
    for name in args:
        length += len(re.sub(r'[^a-zA-Z]', '', name))

    return length