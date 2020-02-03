from .pkgspec import PkgSpec
from .specobject import SpecObject
from .err import ConfigFail
from metux.log import warn

"""Target configuration"""
class TargetSpec(SpecObject):

    """[private]"""
    def __init__(self, name, pool, conf, spec):
        SpecObject.__init__(self, spec)
        self.pool = pool
        self.conf = conf
        self.set_cf_missing('config.basedir', conf['config.basedir'])
        self.set_cf_missing('config.prefix', conf['config.prefix'])
        self.set_cf_missing('target.name', name)
        self.set_cf_missing('target.aptrepo', lambda: self.get_aptrepo_path())
        self.set_cf_missing('target.zyprepo', lambda: self.get_zyprepo_path())
        self.set_cf_missing('pool.name', lambda: 'global' if self.pool is None else self.pool['pool.name'])

    def get_aptrepo_path(self):
        if self.pool is None:
            raise ConfigFail("no pool - dont have an aptrepo")
        else:
            return self.pool['pool.aptrepo']

    def get_zyprepo_path(self):
        if self.pool is None:
            raise ConfigFail("no pool - dont have an zyprepo")
        else:
            return self.pool['pool.zyprepo']

    """allocate a statfile object for the (per target) package build finish-marker"""
    def get_pkg_build_statfile(self, pkg):
        if isinstance(pkg,PkgSpec):
            pkgname = pkg.name
        else:
            pkgname = pkg

        return self.conf.get_statfile(
            "build."+self['pool.name']+"."+self['target.name']+"."+pkgname)

    def get_packager(self):
        p = self.get_cf('packager', None)
        if p is None:
            warn("Target %s has no packager specified. Defaulting to apt" % self['target.name'])
            return 'apt'
        return p
