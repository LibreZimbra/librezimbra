import yaml
from os import getuid
from os.path import expanduser
from metux.log import info

class SpecObject(object):

    """[private]"""
    def __init__(self, spec):
        self._my_spec = spec

    """retrieve a config element by path"""
    def get_cf(self, p, dflt = None):
        node = self._my_spec
        if type(p) == list:
            for walk in p:
                if walk not in node:
                    return dflt
                else:
                    node = node[walk]
            return node
        else:
            if p in node:
                return node[p]
            else:
                return dflt


    """retrieve a config element as list"""
    def get_cf_list(self, p, dflt = []):
        return self.get_cf(p, dflt)

    """retrieve a config element by path and substitute variables"""
    def get_cf_subst(self, p, dflt = None):
        val = self.get_cf(p, dflt)
        if val is None:
            return val
        return self.cf_substvar(val)

    """set spec object"""
    def set_spec(self, s):
        self._my_spec = s

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

    """[override] variable substitution callback"""
    def cf_substvar(self, var):
        if (var is None) or (isinstance(var,bool)):
            return var

        var = var.replace('${user.uid}', str(getuid()))
        var = var.replace('${user.home}', expanduser('~'))

        return var
