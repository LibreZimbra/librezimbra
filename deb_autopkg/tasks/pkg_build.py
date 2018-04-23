from deb_autopkg.util.task import Task

import pkg_build_target

class PkgBuildTask(Task):

    """[private]"""
    def get_targets(self):
        if self.param['pool'] is None:
            return self.param['pkg'].get_conf().get_targets()
        else:
            return self.param['pool'].get_targets()

    """[override]"""
    def get_subtasks(self):
        tasks = []
        for t in self.get_targets():
            tasks.append(pkg_build_target.alloc(self.param['pkg'].get_conf(), self.param['pkg'], t))
        return tasks

def alloc(conf, pkg, pool):
    if pool is None:
        pn = "global"
    else:
        pn = pool.name

    return conf.cached_task_alloc('build-pkg:'+pn+":"+pkg.name, PkgBuildTask, { 'pkg': pkg, 'pool': pool })
