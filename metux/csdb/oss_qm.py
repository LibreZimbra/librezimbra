import yaml
import base

class OSSQMSpec(base.BaseSpec):
    def __type(self):
        return "oss-qm"

class DB(base.BaseDB):

    def __type(self):
        return "oss-qm"

    def __alloc(self, yml):
        return OSSQMSpec(yml)
