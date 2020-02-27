from inspect import isfunction
from collections import Mapping

class LambdaDict(dict):
    def __init__(self, d):
        dict.__init__(self, d)

    def __getitem__(self, key):
        item = dict.__getitem__(self, key)

        if isfunction(item):
            return item()

        if isinstance(item, Mapping):
            return LambdaDict(item)

        return item
