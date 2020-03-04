import yaml
from os import getcwd
from ..util.task import Task
from ..util.statfile import StatFile
from .targetspec import TargetSpec
from .specobject import SpecObject
from .poolspec import PoolSpec
from .pkgspec import PkgSpec
from .dutspec import DutSpec
from metux.csdb import CSDB
from metux.log import info, warn, err
from .err import ConfigFail

"""global configuration"""
class Config(SpecObject):

    """[private]"""
    def __init__(self):
        SpecObject.__init__(self, {})
        self._my_pkg_cache = {}
        self._my_pool_cache = {}
        self._my_task_cache = {}
        self._my_basedir = getcwd()
        self._my_dut_cache = {}
        self._my_targets = {}
        self.__intrinsics()

    def __intrinsics(self):
        self.set_cf_missing('config.basedir', '${user.cwd}')
        self.set_cf_missing('config.prefix',  '${config.basedir}/cf')

    """load a target config"""
    def load_target(self, name, pool):
        fn = 'cf/targets/%s.yml' % name
        try:
            with open(fn) as f:
                spec = yaml.safe_load(f)
                info("loaded target config: "+fn)
                self._my_targets[name] = TargetSpec(name, pool, self, spec)
        except:
            info("failed to load target config: "+fn)
            self._my_targets[name] = TargetSpec(name, pool, self, {})
        return self._my_targets[name]

    """load a global config file"""
    def load(self, fn):
        self.load_spec(fn)
        self.__intrinsics()

        self.csdb = CSDB(self.get_pathconf('csdb-path'), self[['csdb', 'sections']])

        # load target configs
        for t in self.get_cf('targets'):
            self._my_targets[t] = self.load_target(t, None)

    """get package object by name"""
    def get_package(self, name):
        if name in self._my_pkg_cache:
            return self._my_pkg_cache[name]

        pkgs = self.get_package_list()
        if name in pkgs:
            self._my_pkg_cache[name] = PkgSpec(name, pkgs[name], self)
            return self._my_pkg_cache[name]

        return None

    """get list of package names"""
    def get_package_list(self):
        return self.get_cf('packages')

    def get_packages_by_names(self, lst):
        pkgs = []
        for name in lst:
            p = self.get_package(name)
            if p is None:
                raise ConfigFail("missing package spec for "+name)
            else:
                pkgs.append(self.get_package(name))
        return pkgs

    """get list of package objects"""
    def get_packages(self):
        return self.get_packages_by_names(self.get_package_list())

    """[private]"""
    def _cf_dckbp(self, key, dflt, wmsg):
        cf = self.get_cf(['dck-buildpackage', key])
        if cf is None:
            warn(wmsg)
            return dflt
        return cf

    """get builtin docker-buildpackage pkg config object"""
    def get_dckbp_package(self):
        my_url = self._cf_dckbp(
            'git-url',
            'git@github.com:metux/docker-buildpackage.git',
            'dck-buildpackage.git-repo not defined. using default')

        my_branch = self._cf_dckbp(
            'git-branch',
            'master',
            "dck-buildpackage.git-repo not defined. assuming 'master'")

        return PkgSpec(
            '__dckbp',
            { 'my-url':           my_url,
              'my-branch':        my_branch,
              'autobuild-branch': 'my/'+my_branch },
            self)

    """get dck-buildpackage path"""
    def get_dckbp_path(self):
        return ("%s/pkg/__dckbp__.git" % self['config.basedir'])

    """get dck-buildpackage command"""
    def get_dckbp_cmd(self):
        return self.get_dckbp_path()+"/dck-buildpackage"

    """get git repo config"""
    def get_dckbp_gitcf(self):
        my_url = self._cf_dckbp(
            'git-url',
            'git@github.com:metux/docker-buildpackage.git',
            'dck-buildpackage.git-repo not defined. using default')

        my_branch = self._cf_dckbp(
            'git-branch',
            'master',
            "dck-buildpackage.git-repo not defined. assuming 'master'")

        return {
            'path':        self.get_dckbp_path(),
            'remotes':     { 'my': { 'url': my_url, 'branch': my_branch } },
            'init-branch': 'autobuild',
            'init-ref':    'my/'+my_branch
        }

    """get list of pool names"""
    def get_pool_list(self):
        return self.get_cf('pools', [])

    """get pool object by name"""
    def get_pool(self, name):
        if name in self._my_pool_cache:
            return self._my_pool_cache[name]

        pl = self.get_pool_list()
        if name in pl:
            self._my_pool_cache[name] = PoolSpec(name, pl[name], self)
            return self._my_pool_cache[name]

        return None

    """get list of pool objects"""
    def get_pools(self):
        pools = []
        for name in self.get_pool_list():
            pools.append(self.get_pool(name))
        return pools

    """get list of target names"""
    def get_target_list(self):
        return self.get_cf('targets', [])

    """get target objects w/o pool"""
    def get_targets(self):
        tl = []
        for tn in self.get_target_list():
            tl.append(self.load_target(tn, None))
        return tl

    """get a task object from dedup cache"""
    def cached_task_get(self, key):
        if key in self._my_task_cache:
            return self._my_task_cache[key]
        else:
            return None

    """put a task object into dedup cache"""
    def cached_task_put(self, key, tsk):
        self._my_task_cache[key] = tsk

    """allocate task object by key and class or take it from dedup cache"""
    def cached_task_alloc(self, key, cls, param):
        cached = self.cached_task_get(key)
        if cached == None:
            param['name'] = key
            param['conf'] = self
            cached = cls(param)
            self.cached_task_put(key, cached)

        if not isinstance(cached, Task):
            raise ConfigFail("cached task is not a Task")

        return cached

    """get a statfile instance by given name"""
    def get_statfile(self, name):
        return StatFile(name, self._my_basedir)

    """get a path config"""
    def get_pathconf(self, name, default = None):
        return self.get_cf(['pathes', name], default)

    """get list of remotes"""
    def get_remote_names(self):
        r = self.get_pathconf('remote-names')
        if r is not None:
            return r
        return [ "my", "upstream", "debian", "oss-qm" ]

    """retrieve / load DUT configuration"""
    def get_dut(self, name):
        if name in self._my_dut_cache:
            return self._my_dut_cache

        fn = self.get_pathconf('dut-path', 'cf/dut')+"/"+name+".cf"

        with open(fn) as f:
            cf = yaml.safe_load(f)
            info("loaded config: "+fn)
            return DutSpec(name, cf, self)

        raise ConfigFail("missing dut config: "+fn)
