# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

from metux.util.task import Task, TaskFail
from metux.util.git import GitRepo

"""Task: clone an git repo w/ initial checkout"""
class GitCloneTask(Task):

    def do_run(self):

        spec = self.param['spec']
        repo = GitRepo(spec['path'])
        repo.initialize()

        for remote in spec['remotes']:
            repo.set_remote(remote, spec['remotes'][remote]['url'])

        if repo.is_checked_out():
            if ('init-force' in spec) and spec['init-force']:
                self.log_info("forcing re-init to "+spec['init-ref'])
                repo.remote_update_all()
                repo.force_checkout(spec['init-ref'], spec['init-branch'])
            if ('remote-update' in spec) and spec['remote-update']:
                repo.remote_update_all()
        else:
            if (not 'init-ref' in spec) or (spec['init-ref'] is None):
                raise TaskFail(self, 'cant checkout "'+spec['path']+'": autobuild-ref not defined')
            else:
                self.log_info("running initial checkout of "+spec['init-ref'])
                if not repo.checkout(spec['init-ref'], spec['init-branch']):
                    raise TaskFail(self, 'cant checkout "'+spec['path']+'": git checkout failed')

        if spec.get('init-submodules', False):
            self.log_info("initializing submodules")
            repo.submodule_init()

        return True
