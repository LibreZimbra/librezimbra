# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

from ..util.tasks_git import GitCloneTask

def alloc(conf):
    return conf.cached_task_alloc('clone-dck-buildpackage', GitCloneTask, { 'spec': conf.get_dckbp_gitcf() })
