# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

from metux.util.task import Task
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
        self.statfile = self.target.get_pkg_build_statfile(self.pkg)

    def do_run(self):
        pkg_name    = self.pkg.name
        target_name = self.target['target.name']
        pool_name   = self.target['pool.name']
        dckbp_cmd   = self.conf.get_dckbp_cmd()

        env = copy(environ)
        env['DCK_BUILDPACKAGE_TARGET_REPO'] = self.target['target.aptrepo']
        env['DCK_BUILDPACKAGE_SOURCE'] = pkg_name

        self.log_info('building "'+pkg_name+'" from '+pool_name+' for '+target_name)
        if (call([dckbp_cmd, '--target', target_name],
                 cwd=self.pkg['package.src'],
                 env=env) != 0):
            self.fail("build failed: "+pkg_name)

        self.statfile.set(self.pkg.git_repo().get_head_commit())
        return True

    """[override]"""
    def need_run(self):
        return not self.statfile.check(self.pkg.git_repo().get_head_commit())

def alloc(conf, pkg, target):
    return conf.cached_task_alloc('build-pkg-apt:'+target['target.name']+':'+pkg.name, PkgBuildAptTask, { 'pkg': pkg, 'target': target })
