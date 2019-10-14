from subprocess import call, Popen, PIPE
from os import devnull
from os.path import abspath

class GitRepo(object):

    def __init__(self, path):
        self.path = abspath(path)
        self.devnull = open(devnull, 'w')

    def get_config(self, key):
        proc = Popen(["git", "config", key], stdout=PIPE, cwd=self.path)
        (out, err) = proc.communicate()
        return out.strip()

    def set_config(self, key, value):
        if self.get_config(key) == value:
            return False
        else:
            call(['git', 'config', key, value], cwd=self.path)
            return True

    def initialize(self):
        return call(['git', 'init', self.path])

    def set_remote(self, name, url):
        # need to do that complicated to defeat shortcut evaluation
        a = self.set_config('remote.'+name+'.url', url)
        b = self.set_config('remote.'+name+'.fetch', '+refs/heads/*:refs/remotes/'+name+'/*')
        if (a or b):
            return call(['git', 'remote', 'update', name], cwd=self.path)

    def get_symbolic_ref(self, name):
        proc = Popen(["git", "symbolic-ref", name], stdout=PIPE)
        (out, err) = proc.communicate()
        return out

    def is_checked_out(self):
        return (call(
            ['git', 'rev-parse', '--verify', 'HEAD'],
            cwd=self.path,
            stdout=self.devnull,
            stderr=self.devnull) == 0)

    def checkout(self, ref, branch):
        return call(['git', 'checkout', ref, '-b', branch], cwd=self.path)
