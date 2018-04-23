from targetspec import TargetSpec

"""Pool configuration"""
class PoolSpec(object):

    """[private]"""
    def __init__(self, name, spec, conf):
        self.name = name
        self._my_spec = spec
        self.conf = conf

    def get_conf(self):
        return self.conf

    """retrieve a list of package names"""
    def get_package_list(self):
        return self._my_spec['packages']

    """retrieve a list of target names"""
    def get_target_list(self):
        if 'targets' in self._my_spec:
            return self._my_spec['targets']
        else:
            return self.conf.get_target_list()

    """retrieve list of PkgSpec instances"""
    def get_packages(self):
        packages = []
        names = self.get_package_list()
        for n in names:
            p = self.conf.get_package(n)
            if p is None:
                raise Exception("pool "+self.name+" references undefined package: "+n)
            packages.append(p)
        return packages

    """retrieve target objects for this pool"""
    def get_targets(self):
        tl = []
        for tn in self.get_target_list():
            tl.append(TargetSpec(tn, self))
        return tl
