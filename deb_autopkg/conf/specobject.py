import yaml
from os import getuid, getcwd, getgid
from os.path import expanduser
from metux.log import info
from metux.lambdadict import LambdaDict
from string import Template

class SubstTemplate(Template):
    idpattern = r"[_a-zA-Z][_a-zA-Z0-9/\.\-\:]*"

class SpecObject(object):

    """[private]"""
    def __init__(self, spec):
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
        self.default_addlist({
            'user.uid':  lambda: str(getuid()),
            'user.gid':  lambda: str(getgid()),
            'user.home': lambda: expanduser('~'),
            'user.cwd':  lambda: getcwd(),
        })

    """get spec object"""
    def get_spec(self, s):
        return self._my_spec

    """def load spec from yaml"""
    def load_spec(self, fn):
        with open(fn) as f:
            # use safe_load instead load
            self.set_spec(yaml.safe_load(f))
            info("loaded config: "+fn)

    """add a default value, which will be used if key is not present"""
    def default_set(self, key, val):
        self._my_spec.default_set(key, val)

    """add a list of default values"""
    def default_addlist(self, attrs):
        self._my_spec.default_addlist(attrs)

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
