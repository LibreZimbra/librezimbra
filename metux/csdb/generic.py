
from base import BaseSpec, BaseDB

class Spec(BaseSpec):
    def __type(self):
        return self.dbname

    def __init__(self, yml, dbname):
        self.dbname = dbname
        BaseSpec.__init__(self, yml)

class DB(BaseDB):

    def __init__(self, pathname, dbname):
        self.dbname = dbname
        BaseDB.__init__(self, pathname)

    def __type(self):
        return self.dbname

    def __alloc(self, yml):
        return Spec(yml, self.dbname)
