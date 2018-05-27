def colorize(txt, color):
    color_map = {
        'red': '\033[31m',
        'green': '\033[32m',
        'end': '\033[0m'
    }

    if not isinstance(txt, str):
        raise TypeError
    if color not in color_map:
        raise Exception

    return color_map[color] + txt + color_map['end']
