__all__ = [ "log" ]

"""get attribute from container or default if not set"""
def get_attr_def(cnt, name, dflt = None):
    if name in cnt:
        if cnt[name] is not None:
            return cnt[name]
    return dflt
