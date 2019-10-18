__all__ = [ "log" ]

"""transform a list to printable text via given transform function"""
def list2text(data, func):
    return "\n".join(map(func, data))

"""transform a dict to printable text via given transform function"""
def dict2text(data, func):
    return "\n".join(map(func, data.values()))
