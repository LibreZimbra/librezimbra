from inspect import isfunction
from collections import Mapping

class LambdaDict(dict):
    def __init__(self, d, dflt = {}):
        dict.__init__(self, d)
        self.defaults = dict(dflt)

    def __getitem_raw__(self, key):
        if dict.has_key(self, key):
            return dict.__getitem__(self, key)

        if key in self.defaults:
            return self.defaults[key]

        return None

    def __getitem_processed__(self, key):
        item = self.__getitem_raw__(key)

        if callable(item):
            return item()

        if isinstance(item, Mapping):
            return LambdaDict(item)

        return item

    def __getitem__(self, key):
        if type(key)==tuple or type(key)==list:
            if len(key) == 1:
                return self.__getitem_processed__(key[0])

            item = self.__getitem_processed__(key[0])
            if item is None:
                return None

            return item[key[1:]]

        return self.__getitem__(key.split('::'))

    def has_key(self, key):
        if dict.has_key(self, key):
            return True

        if (self.defaults.has_key(key)):
            return True

        return False

    """set a default value, which is returned when key not found"""
    def default_set(self, key, value):
        self.defaults[key] = value

    """remove a default value"""
    def default_del(self, key):
        self.defaults.pop(key, None)

    """add a list of default values"""
    def default_addlist(self, attrs):
        if attrs is not None:
            for key in attrs:
                self.defaults[key] = attrs[key]
