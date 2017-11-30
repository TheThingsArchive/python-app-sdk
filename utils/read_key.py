def read_key(filename):
    with open(filename, 'r') as key_file:
        key = key_file.read()
        return key
