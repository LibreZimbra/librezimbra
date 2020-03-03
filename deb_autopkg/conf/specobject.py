import yaml
from os import getuid, getcwd, getgid
from os.path import expanduser
from metux.log import info
from metux.lambdadict import LambdaDict
from string import Template

class SubstTemplate(Template):
    idpattern = r"[_a-z][_a-z0-9/\.\-]*"

class SpecObject(object):

    """[private]"""
    def __init__(self, spec):
        self.set_spec(spec)

    """retrieve a config element by path"""
    def get_cf_raw(self, p, dflt = None):
        node = self._my_spec
        if (type(p) == list) or (type(p) == tuple):
            for walk in p:
                if walk not in node:
                    return dflt
                else:
                    node = node[walk]
            return node
        else:
            return self.get_cf_raw(p.split('::'), dflt)

    """retrieve a config element as list"""
    def get_cf_list(self, p, dflt = []):
        return self.get_cf(p, dflt)

    """retrieve a config element by path and substitute variables"""
    def get_cf(self, p, dflt = None):
        return self.cf_substvar(self.get_cf_raw(p, dflt))

    """container get method"""
    def __getitem__(self, p):
        return self.get_cf(p)

    """set spec object"""
    def set_spec(self, s):
        self._my_spec = LambdaDict(s)
        self.set_cf_missing('user.uid',  lambda: str(getuid()))
        self.set_cf_missing('user.gid',  lambda: str(getgid()))
        self.set_cf_missing('user.home', lambda: expanduser('~'))
        self.set_cf_missing('user.cwd',  lambda: getcwd())

    """get spec object"""
    def get_spec(self, s):
        return self._my_spec

    """def load spec from yaml"""
    def load_spec(self, fn):
        with open(fn) as f:
            # use safe_load instead load
            self.set_spec(yaml.safe_load(f))
            info("loaded config: "+fn)

    """set attribute if not existing yet (doesnt support path yet)"""
    def set_cf_missing(self, attr, val):
        if val is not None:
            if (attr not in self._my_spec) or (self._my_spec[attr] is None):
                self._my_spec[attr] = val

    """set list (dict) of attribute if not existing yet (doesnt support path yet)"""
    def set_cf_missing_list(self, attrs):
        for name in attrs:
            self.set_cf_missing(name, attrs[name])

    """[private] variable substitution"""
    def cf_substvar(self, var):
        if (var is None) or (isinstance(var,bool)) or (isinstance(var, (long, int))):
            return var

        if isinstance(var, basestring) or (isinstance(var, str)):
            if var.lower() in ['true', '1', 't', 'y', 'yes']:
                return True

            if var.lower() in ['false', '0', 'f', 'n', 'no']:
                return False

            new = SubstTemplate(var).substitute(self._my_spec)
            if new == var:
                return var

            return self.cf_substvar(new)

        return var
