__all__ = [ "log" ]

"""get attribute from container or default if not set"""
def get_attr_def(cnt, name, dflt = None):
    if name in cnt:
        if cnt[name] is not None:
            return cnt[name]
    return dflt

"""transform a list to printable text via given transform function"""
def list2text(data, func):
    return "\n".join(map(func, data))

"""transform a dict to printable text via given transform function"""
def dict2text(data, func):
    return "\n".join(map(func, data.values()))
