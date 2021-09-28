from inspect import isfunction
from collections import Mapping, MutableSequence
from metux.util.log import info

def isarray(item):
    return isinstance(item, tuple) or isinstance(item, MutableSequence)

class LambdaBase:
    def filter_new_item(self, item):
        if isinstance(item, Mapping):
            return LambdaDict(item, None, filter = self.filter)
        if isinstance(item, MutableSequence):
            return LambdaList(item, filter = self.filter)
        return item

class LambdaDictFilter:
    def filter_get_res(self, ld, key, val):
        return val

class LambdaList(MutableSequence, LambdaBase):
    def __init__(self, lst, filter = None):
        MutableSequence.__init__(self)
        self.filter = filter
        self.my_list = list()
        if lst is not None:
            for elem in lst:
                self.append(elem)

    def __str__(self):
        return "LambdaList: "+str(self.my_list)

    def __len__(self):
        return len(self.my_list)

    def __getitem__(self, i):
        return self.my_list[i]

    def __delitem__(self, i):
        del self.my_list[i]

    def __setitem__(self, i, v):
        self.my_list[i] = self.filter_new_item(v)

    def append(self, v):
        self.my_list.append(self.filter_new_item(v))

    def insert(self, i, v):
        self.my_list.insert(i, self.filter_new_item(v))

class LambdaDict(dict,LambdaBase):
    def __init__(self, d = None, dflt = None, filter = None):
        self.filter = filter
        self.load_dict(d)
        if dflt is None:
            dflt = {}
        self.defaults = dict(dflt)

    def load_dict(self, d):
        if d is not None:
            for k,v in d.items():
                dict.__setitem__(self, k, self.filter_new_item(v))

    def __getitem_raw__(self, key):
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)

        if key in self.defaults:
            return self.defaults[key]

        return None

    def __getitem__(self, key):
        if isarray(key):

            # fetch item from dict
            item = self.__getitem_raw__(key[0])

            # process potential callable
            if callable(item):
                item = item()

            # apply filter
            if self.filter is not None:
                item = self.filter.filter_get_res(self, key[0], item)

            # break out of end of keys or None
            if len(key) == 1 or item is None:
                return item

            # ask our child dict
            return item[key[1:]]

        return self.__getitem__(key.split('::'))

    def __contains__(self, key):
        if dict.__contains__(self, key):
            return True

        if (self.defaults.__contains__(key)):
            return True

        return False

    def __mksub(self, key):
        if dict.__contains__(self, key):
            sub = dict.__getitem__(self, key)
            if not isinstance(sub, Mapping):
                raise Exeption("attemted to add default for a sub-dict defined as scalar")
            return sub

        sub = LambdaDict(None, None, self.filter)
        dict.__setitem__(self, key, sub)
        return sub

    """set a default value, which is returned when key not found"""
    def default_set(self, key, value):
        if isarray(key):
            k0 = key[0]
            if len(key) == 1:
                self.defaults[k0] = value
            else:
                self.__mksub(k0).default_set(key[1:], value)
        else:
            self.default_set(key.split('::'), value)

    """remove a default value"""
    def default_del(self, key):
        self.defaults.pop(key, None)

    """add a list of default values"""
    def default_addlist(self, attrs):
        if attrs is not None:
            for key, value in attrs.items():
                self.default_set(key, value)

    """add item to the dict (not default)"""
    def __setitem__(self, key, value):
        if isarray(key):

            if len(key) == 1: # final leaf
                dict.__setitem__(self, key[0], value)
                return

            if dict.__contains__(self, key[0]):
                sub = dict.__getitem__(self, key[0])
                if not isinstance(sub, Mapping):
                    raise Exception("cant add elements to non-dict")
            else:
                sub = LambdaDict({}, None, self.filter)
                dict.__setitem__(self, key[0], self.filter_new_item(sub))

            return sub.__setitem__(key[1:], value)

        return self.__setitem__(key.split('::'), value)
