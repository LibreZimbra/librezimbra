from deb_autopkg.util.task import Task, TaskFail
from metux.git import GitRepo
from deb_autopkg.util.log import warn, info

"""Task: clone an git repo w/ initial checkout"""
class GitCloneTask(Task):

    def do_run(self):

        spec = self.param['spec']
        repo = GitRepo(spec['path'])
        repo.initialize()

        for remote in spec['remotes']:
            repo.set_remote(remote, spec['remotes'][remote]['url'])

        if not repo.is_checked_out():
            if (not 'init-ref' in spec) or (spec['init-ref'] is None):
                warn('cant checkout "'+spec['path']+'": autobuild-branch not defined')
            else:
                info("running initial checkout of "+spec['init-ref'])
                repo.checkout(spec['init-ref'], spec['init-branch'])

        return True
