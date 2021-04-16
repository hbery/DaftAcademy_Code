import re

search = re.compile(r'[^\W\d]', re.UNICODE)

def calculate_names_length(*args, **kwargs):
    length = 0
    for name in args:
        length += len(search.findall(name))

    return length

if __name__ == "__main__":
    print(calculate_names_length('Świstak', "parówa123&*(*(&^% -"))