from metux.log import info
from subprocess import call

"""DUT configuration"""
class DutSpec(object):

    """[private]"""
    def __init__(self, name, spec, conf):
        self.name = name
        self._my_spec = spec
        self.conf = conf

    """retrieve toplevel config object"""
    def get_conf(self):
        return self.conf

    """get the target identifier of this DUT"""
    def get_target_name(self):
        return self._my_spec.get('target')

    """shall we reboot after deployment ?"""
    def get_post_deploy_reboot(self):
        if 'post-deploy' in self._my_spec:
            return self._my_spec['post-deploy'].get('reboot', False)
        return False

    """execute command on DUT"""
    def dut_exec(self, cmd):
        hostname = self._my_spec['ssh']['hostname']
        username = self._my_spec['ssh']['username']
        port = str(self._my_spec['ssh']['port'])

        info("executing on DUT: %s" % repr(cmd))

        return (call([
            'ssh',
            ("%s@%s" % (username, hostname)),
            '-p',
            port,
            '--'
        ] + cmd)==0)

    """run apt-get update && apt-get upgrade on DUT"""
    def apt_upgrade(self):
        return (self.dut_exec(["apt-get", "update"]) and
                self.dut_exec(["apt-get", "upgrade", "-y"]))

    """install packages"""
    def apt_install(self, pkg):
        if isinstance(pkg, str):
            pkg = [ pkg ]

        return self.dut_exec(["apt-get", "install", "-y"] + pkg)

    """reboot the dut"""
    def reboot(self):
        return self.dut_exec(["reboot"])
