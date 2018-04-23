from deb_autopkg.util.tasks_git import GitCloneTask

def alloc(conf):
    return conf.cached_task_alloc('clone-dck-buildpackage', GitCloneTask, { 'spec': conf.get_dckbp_gitcf() })
