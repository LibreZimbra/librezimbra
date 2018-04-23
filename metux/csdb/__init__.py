
__all__ = [ "upstream" ]

import debian
import upstream
import oss_qm

class CSDB:
    def __init__(self, confpath):
        self.confpath = confpath
        self.upstream = upstream.DB(confpath+"/upstream")
        self.debian   = debian.DB(confpath+"/debian")
        self.oss_qm   = oss_qm.DB(confpath+"/oss-qm")

    def get_upstream(self, pkg):
        return self.upstream.get(pkg)

    def get_debian(self, pkg):
        return self.debian.get(pkg)

    def get_oss_qm(self, pkg):
        return self.oss_qm.get(pkg)
