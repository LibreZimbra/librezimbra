from ..util.task import Task
from ..util.upload import run_upload

"""Target: upload a whole pool of packages to testbox / repo server"""
class PoolUploadTask(Task):

    """[override]"""
    def do_run(self):
        upload = self.param['pool'].get_upload()
        if upload is None:
            self.log_info("no upload specified")
            return True

        return run_upload({
            'protocol': upload.get('protocol'),
            'username': upload.get('username', None),
            'hostname': upload.get('hostname', None),
            'path':     upload.get('path', None),
            'source':   self.param['pool'].get_aptrepo_path(),
        })

def alloc(conf, pool):
    return conf.cached_task_alloc('upload-pool:'+pool.name, PoolUploadTask, { 'pool': pool })
