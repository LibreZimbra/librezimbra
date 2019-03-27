import yaml
from sys import stderr
from deb_autopkg.util import get_attr_def
from deb_autopkg.util.log import info, warn

"""Package configuration"""
class PkgSpec(object):

    """[private]"""
    def _map_ext_attr(self, ext, spec_attr, ext_attr):
        if (spec_attr not in self._my_spec) and (ext_attr in ext):
            info("setting "+spec_attr+"="+ext[ext_attr])
            self._my_spec[spec_attr] = ext[ext_attr]

    """[private] set attribute if not existing"""
    def _addattr(self, attr, val):
        if val is not None:
            if (attr not in self._my_spec) or (self._my_spec[attr] is None):
                self._my_spec[attr] = val

    """split package identifier into name and (optional) version"""
    def _split_pkg_version(self, name):
        splitted = name.split('@',1)
        if (len(splitted) > 1):
            return (splitted[0], splitted[1])
        else:
            return (name, None)

    """[private]"""
    def _load_db(self, dbname):
        self._my_db[dbname] = self.conf.csdb.get_db(self.package_name, dbname)
        if self._my_db[dbname] is not None:
            self._addattr(dbname+'-url',    self._my_db[dbname].git_url)
            self._addattr(dbname+'-branch', self._my_db[dbname].git_branch)

    """[private]"""
    def __init__(self, name, spec, conf):
        if spec is None:
            stderr.write("WARN: pkg spec is None for package: "+name+"\n")

        self._my_spec = spec
        self.conf = conf
        self.name = name
        self._my_db = {}

        ## split package name / version
        (self.package_name, self.package_version) = self._split_pkg_version(self.name)

        ## load repo configs from csdb
        for dbn in self.conf.csdb.get_dbnames():
            self._load_db(dbn)

    """[private] substitute variables"""
    def _substvar(self, v):
        if self.package_version is not None:
            v = v.replace('${package.version}', self.package_version)
        v = v.replace('${package.name}', self.package_name)
        return v

    """load a global config file"""
    def load(self, fn):
        with open(fn) as f:
            # use safe_load instead load
            self._my_spec = yaml.safe_load(f)
            info("loaded config: "+fn)

    """[private]"""
    def __cf_str(self, name):
        if name in self._my_spec:
            return self._substvar(self._my_spec[name])
        else:
            return None

    """[private]"""
    def __cf_list(self, name):
        if name in self._my_spec:
            return self._my_spec[name]
        else:
            return []

    """get the global config"""
    def get_conf(self):
        return self.conf

    """get git repo directory"""
    def git_repo_dir(self):
        return 'pkg/' + self.name + '.git'

    """get url of remote repo <name>"""
    def git_remote_url(self, name):
        return self.__cf_str(name+'-url')

    """get the default branch"""
    def get_autobuild_branch(self):
        return self.__cf_str('autobuild-branch')

    """get dependencies - package names)"""
    def get_depends_list(self):
        return self.__cf_list('depends')

    """get dependencies - package objects"""
    def get_depends_packages(self):
        return self.conf.get_packages_by_names(self.get_depends_list())

    """get git repo config"""
    def get_repo_conf(self):
        remotes = {}
        for r in [ "my", "upstream", "debian", "oss-qm" ]:
            u = self.git_remote_url(r)
            if u is not None:
                remotes[r] = { 'url': u }
        return {
            'path':        self.git_repo_dir(),
            'remotes':     remotes,
            'init-branch': 'autobuild',
            'init-ref':    self.get_autobuild_branch() }
