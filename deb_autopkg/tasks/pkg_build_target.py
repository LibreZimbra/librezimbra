from ..util.task import Task
from .pkg_clone import alloc as pkg_clone_alloc
from .dckbp_clone import alloc as dckbp_clone_alloc
from .pkg_build_apt import alloc as pkg_build_apt_alloc
from metux.git import GitRepo

"""Task: build a package for a target"""
class PkgBuildTargetTask(Task):

    """[private]"""
    def __init__(self, param):
        Task.__init__(self, param)
        self.target   = param['target']
        self.conf     = param['conf']
        self.pkg      = param['pkg']
        self.statfile = self.target.get_pkg_build_statfile(self.pkg)

    """[override]"""
    def get_subtasks(self):
        tasks = []
        tasks.append(dckbp_clone_alloc(self.conf))
        tasks.append(pkg_clone_alloc(self.conf, self.pkg))

        for pkg in self.pkg.get_depends_packages():
            tasks.append(alloc(self.conf, pkg, self.target))

        packager = self.target.get_packager()
        if packager == 'apt':
            tasks.append(pkg_build_apt_alloc(self.conf, self.pkg, self.target))
        else:
            self.fail('unknown packager "%s" for target %s' %
                        (packager, self.target.get_target_name()))

        return tasks

    """[override]"""
    def need_run(self):
        return not self.statfile.check(GitRepo(self.pkg.git_repo_dir()).get_head_commit())

    """[override]"""
    def do_run(self):
        self.statfile.set(GitRepo(self.pkg.git_repo_dir()).get_head_commit())
        return True

def alloc(conf, pkg, target):
    return conf.cached_task_alloc('build-pkg-target:'+target.name+':'+pkg.name, PkgBuildTargetTask, { 'pkg': pkg, 'target': target })
