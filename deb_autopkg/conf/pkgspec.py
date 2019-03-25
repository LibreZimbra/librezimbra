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
    def __init__(self, name, spec, conf):
        if spec is None:
            stderr.write("WARN: pkg spec is None for package: "+name+"\n")

        self._my_spec = spec
        self.conf = conf
        self.name = name

        ## split package name / version
        (self.package_name, self.package_version) = self._split_pkg_version(self.name)

        ## load upstream config
        self._my_upstream = self.conf.csdb.get_upstream(self.package_name)
        if self._my_upstream is not None:
            self._addattr('upstream-url',    self._my_upstream.git_url)
            self._addattr('upstream-branch', self._my_upstream.git_branch)

        ## load debian config
        self._my_debian = self.conf.csdb.get_debian(self.package_name)
        if self._my_debian is not None:
            self._addattr('debian-url',      self._my_debian.git_url)
            self._addattr('debian-branch',   self._my_debian.git_branch)

        ## load oss-qm config
        self._my_oss_qm = self.conf.csdb.get_oss_qm(self.package_name)
        if self._my_oss_qm is not None:
            self._addattr('oss-qm-url',      self._my_oss_qm.git_url)
            self._addattr('oss-qm-branch',   self._my_oss_qm.git_branch)

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
