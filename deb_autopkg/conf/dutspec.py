from metux.log import info
from subprocess import call
from .specobject import SpecObject

"""DUT configuration"""
class DutSpec(SpecObject):

    """[private]"""
    def __init__(self, name, spec, conf):
        self.name = name
        self.conf = conf
        self.set_spec(spec)

    """retrieve toplevel config object"""
    def get_conf(self):
        return self.conf

    """get the target identifier of this DUT"""
    def get_target_name(self):
        return self.get_cf('target')

    """shall we reboot after deployment ?"""
    def get_post_deploy_reboot(self):
        return self.get_cf(['post-deploy', 'reboot'], False)

    """execute command on DUT"""
    def dut_exec(self, cmd):
        hostname = self.get_cf(['ssh', 'hostname'])
        username = self.get_cf(['ssh', 'username'])
        port = str(self.get_cf(['ssh', 'port']))

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
