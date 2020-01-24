from ..util.tasks_git import GitCloneTask

def alloc(conf, pkg):
    return conf.cached_task_alloc('clone-pkg:'+pkg.name, GitCloneTask, { 'spec': pkg.get_repo_conf() })
