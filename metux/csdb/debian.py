import yaml
import base

class DebianSpec(base.BaseSpec):
    def __type(self):
        return "Debian"

class DB(base.BaseDB):

    def __type(self):
        return "Debian"

    def __alloc(self, yml):
        return DebianSpec(yml)
