# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

from metux.util.task import Task
from .pkg_build import alloc as pkg_build_alloc

"""Target: build a whole pool of packages"""
class PoolBuildTask(Task):

    """[override]"""
    def get_subtasks(self):
        tasks = []
        pool = self.param['pool']
        conf = pool.get_conf()

        for pkg in pool.get_packages():
            tasks.append(pkg_build_alloc(conf, pkg, pool))

        return tasks

def alloc(conf, pool):
    return conf.cached_task_alloc('build-pool:'+pool['pool.name'], PoolBuildTask, { 'pool': pool })
