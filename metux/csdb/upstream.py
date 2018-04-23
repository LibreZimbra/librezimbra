import yaml
import base

class UpstreamSpec(base.BaseSpec):

    def __type(self):
        return "Upstream"

class DB(base.BaseDB):

    def __type(self):
        return "upstream"

    def __alloc(self, yml):
        return UpstreamSpec(yml)
