import yaml
from metux.util.log import info
from metux.util.lambdadict import LambdaDict, LambdaDictFilter
from string import Template
from collections import MutableSequence
import re

try:
    my_basestring = basestring
except:
    my_basestring = str

class SubstTemplate(Template):
    idpattern = r"[_a-zA-Z][_a-zA-Z0-9/\.\-\:]*"
    match_re = re.compile(r'^\$\{([_a-zA-Z][_a-zA-Z0-9/\.\-\:]*)\}$')

class SpecError(Exception):

    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, "[spec error] "+msg)

    def get_message(self):
        return self.msg

class SpecObjectFilter(LambdaDictFilter):
    def __init__(self, specobj):
        self.specobj = specobj

    """[private]"""
    def filter_get_res(self, ld, key, value):
        return self.subst(value)

    def subst(self, value):
        if isinstance(value, my_basestring) or (isinstance(value, str)):
            res = SubstTemplate.match_re.match(value.strip())
            if res is not None:
                newkey = res.group(1)
                return self.subst(self.specobj[newkey])

            if "${" in value:
                new = SubstTemplate(value).substitute(self.specobj._my_spec)
                if new == value:
                    return value
                else:
                    return self.subst(new)

        if isinstance(value, MutableSequence):
            return [self.subst(x) for x in value]

        return value

class SpecObject(object):

    """[private]"""
    def __init__(self, spec):
        self.filter = SpecObjectFilter(self)
        self.set_spec(spec)

    """retrieve a config element by path"""
    def get_cf_raw(self, p, dflt = None):
        res = self._my_spec[p]
        if res is None:
            return dflt
        else:
            return res

    """retrieve a config element as list"""
    def get_cf_list(self, p, dflt = []):
        x = self.get_cf(p, dflt)
        if x is not None:
            if isinstance(x, MutableSequence):
                return x
            return [x]

    """retrieve a config element by path and substitute variables"""
    def get_cf(self, p, dflt = None):
        if not (isinstance(p, MutableSequence) or isinstance(p, tuple)):
            return self.get_cf(p.split('::'), dflt)

        walk = self._my_spec
        for pwalk in p:
            walk = walk[pwalk]
            if walk is None:
                return dflt
        return walk

    """retrieve a config element as dict"""
    def get_cf_dict(self, p):
        r = self.get_cf(p)
        if p is None:
            return LambdaDict({})
        return r

    """retrieve a config element as bool"""
    def get_cf_bool(self, p, dflt = False):
        r = self.get_cf(p, dflt)
        if r is None:
            return dflt
        if r:
            return True
        return False

    """container get method"""
    def __getitem__(self, p):
        return self.get_cf(p)

    """container set method"""
    def __setitem__(self, key, val):
        self._my_spec[key] = val

    """container has_key method"""
    def has_key(self, p):
        return self._my_spec.has_key(p)

    """set spec object"""
    def set_spec(self, s):
        self._my_spec = LambdaDict(s, None, self.filter)
        self.post_init()

    """get spec object"""
    def get_spec(self, s):
        return self._my_spec

    """def load spec from yaml"""
    def load_spec(self, fn):
        with open(fn) as f:
            # use safe_load instead load
            self.set_spec(yaml.load(f, yaml.CSafeLoader))
            info("loaded config: "+fn)

    """add a default value, which will be used if key is not present"""
    def default_set(self, key, val):
        self._my_spec.default_set(key, val)

    """add a list of default values"""
    def default_addlist(self, attrs):
        self._my_spec.default_addlist(attrs)

    """check for mandatory attributes"""
    def check_mandatory(self, attrs):
        for a in attrs:
            if not self.has_key(a):
                raise Exception("missing mandatory attribute %s" % a)

    def post_init(self):
        pass
