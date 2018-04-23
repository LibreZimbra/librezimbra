from util.task import TaskRunner
from tasks import pkg_build, pkg_clone, all_clone, pool_build

class Builder:

    def __init__(self, conf):
        self.conf = conf

    def _run(self, task):
        return TaskRunner(task.name).runTask(task)

    def build_package(self, name):
        return self._run(pkg_build.alloc(self.conf, self.conf.get_package(name)))

    def clone_package(self, name):
        return self._run(pkg_clone.alloc(self.conf, self.conf.get_package(name)))

    def clone_all(self):
        return self._run(all_clone.alloc(self.conf))

    def build_pool(self, name):
        pool = self.conf.get_pool(name)
        if pool is None:
            raise Exception("undefined pool: "+name)
        return self._run(pool_build.alloc(self.conf, self.conf.get_pool(name)))

    def build_all(self):
        return self._run(build_all.alloc(self.conf))
