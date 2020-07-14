from metux.util.log import info
from subprocess import call, Popen, PIPE

class SchrootSession:
    def __init__(self, chroot_name, user):
        self.chroot_name = chroot_name
        self.user = user

        ## create a new session
        args = [ 'schroot', '-b', '-c', chroot_name ]
        (out, err) = proc = Popen(args+['--'], stdout=PIPE).communicate()

        self.session_name = out.strip()
        info("created schroot session: %s [user %s]" % (self.session_name, user))

    def remove(self):
        info("removed schroot session: %s" % self.session_name)
        ret = call(['schroot', '-c', self.session_name, '-e', '-f'])
        self.session_name = None

    def _args(self, cmdline, user):
        if user is None:
            user = self.user
        if (user is None) or (user == ''):
            return ['schroot', '-r', '-c', self.session_name, '--']+cmdline
        else:
            return ['schroot', '-u', user, '-r', '-c', self.session_name, '--']+cmdline

    def call(self, cmd, user = None):
        return call(self._args(cmd, user))

    def run(self, cmd, user = None):
        (out, err) = proc = Popen(self._args(cmd),stdout=PIPE).communicate()
        if out is None:
            out = ''
        if err is None:
            err = ''
        info("schroot: out: "+out)
        info("schroot: err: "+err)
        return out

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.remove()

def create_session(chroot, user = None):
    return SchrootSession(chroot, user)
