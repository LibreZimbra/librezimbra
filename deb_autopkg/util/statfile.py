
from os import path, makedirs, unlink

"""helper object for representing a status file"""
class StatFile(object):

    def __init__(self, name, basedir):
        self.name = "%s/.stat/%s" % (basedir, name);

    def _prepare(self):
        dn = path.dirname(self.name)
        if not path.exists(dn):
            makedirs(dn)

    def check(self):
        self._prepare()
        return path.isfile(self.name)

    def set(self):
        self._prepare()
        open(self.name, 'a').close()

    def rm(self):
        unlink(self.name)
