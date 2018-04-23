from deb_autopkg.util.task import Task

import pkg_clone
import dckbp_clone

""" Task: clone all package git repos"""
class CloneAllTask(Task):

    def get_subtasks(self):
        conf = self.param['conf']
        tasks = [ dckbp_clone.alloc(conf) ]
        for pkg in conf.get_packages():
            tasks.append(pkg_clone.alloc(conf, pkg))
        return tasks

def alloc(conf):
    return conf.cached_task_alloc('clone-all', CloneAllTask, { 'conf': conf })
