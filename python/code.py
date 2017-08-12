def is_binary_string(bytes):
    '''Check if bytestring contains binary data

    Source: J.F. Sebastian (https://stackoverflow.com/a/7392391/2514228)
    '''
    textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    return bool(bytes.translate(None, textchars))

def is_binary_file(path):
    '''Check if file contains binary data

    Source: J.F. Sebastian (https://stackoverflow.com/a/7392391/2514228)
    '''
    with open(path, 'rb') as f:
        return is_binary_string(f.read(1024))
