
from os import path, makedirs, unlink

"""helper object for representing a status file"""
class StatFile(object):

    def __init__(self, name, basedir):
        self.name = "%s/.stat/%s" % (basedir, name);

    def _prepare(self):
        dn = path.dirname(self.name)
        if not path.exists(dn):
            makedirs(dn)

    def check(self, value = None):
        self._prepare()
        if value is None:
            return path.isfile(self.name)

        try:
            f = open(self.name, 'r')
            contents = f.read()
            f.close()

            return contents == value
        except:
            return False

    def set(self, value = None):
        self._prepare()
        f = open(self.name, 'w')
        if value is not None:
            f.write(value)
        f.close()

    def rm(self):
        try:
            unlink(self.name)
        except:
            pass
