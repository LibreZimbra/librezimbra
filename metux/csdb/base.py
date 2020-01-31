import yaml
from ..log import info, err, debug

class BaseSpec:

    def __init__(self, spec):
        self._my_spec = spec
        self.git_url = self.__get_spec('git.url')
        self.git_branch = self.__get_spec('git.branch')

    def __type(self):
        return "Base"

    def __getitem__(self, key):
        return self._my_spec[key]

    def has_key(self, key):
        return self._my_spec.has_key(key)

    def __get_spec(self, key):
        if key in self._my_spec:
            return self._my_spec[key]
        else:
            return None

class BaseDB:
    def __init__(self, pathname):
        self.pathname = pathname

    def __type(self):
        return "base"

    def __alloc(self, yml):
        return BaseSpec(yml)

    def get(self, pkg):
        filename = self.pathname+"/"+pkg+".yml"
        try:
            with open(filename) as f:
                try:
                    spec = self.__alloc(yaml.safe_load(f))
                    info("cddb: loaded "+self.__type()+" spec: "+filename)
                    return spec
                except Exception as exc:
                    err("csdb: failed to parse "+self.__type()+" spec: "+filename)
                    print ("execption: "+exc)
                    raise exc
        except IOError:
            debug("csdb: missing "+self.__type()+" spec: "+filename)
            return None
