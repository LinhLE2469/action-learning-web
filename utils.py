from time import strftime
from time import gmtime


def format_seconds(seconds):
    return strftime("%H:%M:%S", gmtime(seconds))


def format_milliseconds(milliseconds):
    return f"{milliseconds * 1000 :.2f} ms"


def get_difference_percentage(a, b):
    return f"{(a - b) / a * 100 :.2f}%"


def size_human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
