from ..util.task import Task
from subprocess import call

"""Target: deploy a whole pool of packages to dut"""
class PoolDeployTask(Task):

    """[override]"""
    def do_run(self):
        pool = self.param['pool']
        dut = pool.get_dut()
        if dut is None:
            self.log_info("no DUT configured - nothing to deploy")
            return True

        self.log_info("Deploying DUT: %s" % dut.name)
        if not (dut.apt_upgrade() and
                dut.apt_install(pool.get_latest_debs(dut.get_target_name()))):
            return False

        if dut.get_post_deploy_reboot():
            return dut.reboot()

        return True

def alloc(conf, pool):
    return conf.cached_task_alloc('deploy-pool:'+pool.name, PoolDeployTask, { 'pool': pool })
