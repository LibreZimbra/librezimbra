from ..util.task import Task

from .pkg_clone import alloc as pkg_clone_alloc
from .dckbp_clone import alloc as dckbp_clone_alloc

""" Task: clone all package git repos"""
class CloneAllTask(Task):

    def get_subtasks(self):
        conf = self.param['conf']
        tasks = [ dckbp_clone_alloc(conf) ]
        for pkg in conf.get_packages():
            tasks.append(pkg_clone_alloc(conf, pkg))
        return tasks

def alloc(conf):
    return conf.cached_task_alloc('clone-all', CloneAllTask, { 'conf': conf })
