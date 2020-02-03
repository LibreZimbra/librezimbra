from .targetspec import TargetSpec
from .specobject import SpecObject
from .err import ConfigFail
from os.path import basename
from metux.log import warn

"""Pool configuration"""
class PoolSpec(SpecObject):

    """[private]"""
    def __init__(self, name, spec, conf):
        SpecObject.__init__(self, spec)
        self.conf = conf
        self.set_cf_missing('config.basedir', conf['config.basedir'])
        self.set_cf_missing('pool.name',      name)
        self.set_cf_missing('pool.aptrepo',   '${config.basedir}/.aptrepo/${pool.name}')
        self.set_cf_missing('pool.zyprepo',   '${config.basedir}/.zyprepo/${pool.name}')

    def get_conf(self):
        return self.conf

    """retrieve a list of package names"""
    def get_package_list(self):
        return self.get_cf('packages')

    """retrieve a list of target names"""
    def get_target_list(self):
        n = self.get_cf('targets')
        if n is None:
            return self.conf.get_target_list()
        else:
            return n

    """retrieve list of PkgSpec instances"""
    def get_packages(self):
        packages = []
        names = self.get_package_list()
        for n in names:
            p = self.conf.get_package(n)
            if p is None:
                raise ConfigFail("pool "+self['pool.name']+" references undefined package: "+n)
            packages.append(p)
        return packages

    """retrieve target objects for this pool"""
    def get_targets(self):
        tl = []
        for tn in self.get_target_list():
            tl.append(self.conf.load_target(tn, self))
        return tl

    """retrieve specific target object for this pool"""
    def get_target(self, name):
        tl = []
        for tn in self.get_target_list():
            if (tn == name):
                return self.conf.load_target(tn, self)
        warn("pool %s: undefined target requested: %s" % (self['pool.name'], name))

    """retrieve uplaod information"""
    def get_upload(self):
        return self.get_cf('upload')

    """retrieve DUT information"""
    def get_dut(self):
        dut = self.get_cf('dut')
        if dut is not None:
            return self.conf.get_dut(dut)

    """get list of recently built debian package names for given package"""
    def get_latest_debs(self, target):
        names = []
        for p in self.get_packages():
            fn = ("%s/%s/stat/%s/latest-debs" % (self['pool.aptrepo'], target, p.name))
            with open(fn) as fp:
                for cnt, debfn in enumerate(fp):
                    names.append(basename(debfn).split('_')[0])

        return names

    """invalidate already built package on given target"""
    def invalidate_target_package(self, pkg, targetname):
        self.get_target(targetname).get_pkg_build_statfile(pkg).rm()
