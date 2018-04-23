from deb_autopkg.util.task import Task

import pkg_build

"""Target: build a whole pool of packages"""
class PoolBuildTask(Task):

    """[override]"""
    def get_subtasks(self):
        tasks = []
        pool = self.param['pool']
        conf = pool.get_conf()

        for pkg in pool.get_packages():
            tasks.append(pkg_build.alloc(conf, pkg, pool))

        return tasks

def alloc(conf, pool):
    return conf.cached_task_alloc('build-pool:'+pool.name, PoolBuildTask, { 'pool': pool })
