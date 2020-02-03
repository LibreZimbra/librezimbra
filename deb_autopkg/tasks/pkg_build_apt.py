from ..util.task import Task
from os import environ
from copy import copy
from subprocess import call

"""build for apt (docker-buildpackage)"""
class PkgBuildAptTask(Task):

    """[private]"""
    def __init__(self, param):
        Task.__init__(self, param)
        self.target   = param['target']
        self.conf     = param['conf']
        self.pkg      = param['pkg']

    def do_run(self):
        pkg_name    = self.pkg.name
        target_name = self.target.get_target_name()
        pool_name   = self.target.get_pool_name()
        dckbp_cmd   = self.conf.get_dckbp_cmd()

        env = copy(environ)
        env['DCK_BUILDPACKAGE_TARGET_REPO'] = self.target.get_aptrepo_path()
        env['DCK_BUILDPACKAGE_SOURCE'] = pkg_name

        self.log_info('building "'+pkg_name+'" from '+pool_name+' for '+target_name)
        if (call([dckbp_cmd, '--target', target_name],
                 cwd=self.pkg.git_repo_dir(),
                 env=env) != 0):
            self.fail("build failed: "+pkg_name)

        return True

def alloc(conf, pkg, target):
    return conf.cached_task_alloc('build-pkg-apt:'+target.name+':'+pkg.name, PkgBuildAptTask, { 'pkg': pkg, 'target': target })
