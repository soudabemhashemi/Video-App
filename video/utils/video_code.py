import string
from datetime import datetime


# todo: refactor these generators.

def generate_video_code():
    timestamp = datetime.now().timestamp()
    timestamp = int(timestamp * 100)
    base = 43

    def get_charset():
        charset = string.digits + string.ascii_letters
        charset = charset[::2] + charset[1::2]
        charset = charset[::2] + charset[1::2]
        charset = charset[1::3] + charset[::3] + charset[2::3]
        return charset

    chars = get_charset()

    if timestamp < 0:
        sign = -1
    elif timestamp == 0:
        return chars[0]
    else:
        sign = 1

    timestamp *= sign
    digits = []

    while timestamp:
        digits.append(chars[int(timestamp % base)])
        timestamp = int(timestamp / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)


def generate_playlist_code():
    timestamp = datetime.now().timestamp()
    timestamp = int(timestamp * 100)
    base = 50

    def get_charset():
        charset = string.digits + string.ascii_letters
        charset = charset[::2] + charset[1::2]
        charset = charset[1::3] + charset[::3] + charset[2::3]
        charset = charset[::2] + charset[1::2]
        charset = charset[1::3] + charset[::3] + charset[2::3]
        return charset

    chars = get_charset()

    if timestamp < 0:
        sign = -1
    elif timestamp == 0:
        return chars[0]
    else:
        sign = 1

    timestamp *= sign
    digits = []

    while timestamp:
        digits.append(chars[int(timestamp % base)])
        timestamp = int(timestamp / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)


def generate_channel_code():
    timestamp = datetime.now().timestamp()
    timestamp = int(timestamp * 100)
    base = 50

    def get_charset():
        charset = string.digits + string.ascii_letters
        charset = charset[::2] + charset[1::2]
        charset = charset[1::3] + charset[::3] + charset[2::3]
        charset = charset[::2] + charset[1::2]
        charset = charset[1::3] + charset[::3] + charset[2::3]
        return charset

    chars = get_charset()

    if timestamp < 0:
        sign = -1
    elif timestamp == 0:
        return chars[0]
    else:
        sign = 1

    timestamp *= sign
    digits = []

    while timestamp:
        digits.append(chars[int(timestamp % base)])
        timestamp = int(timestamp / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)
