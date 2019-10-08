from subprocess import call
import subprocess
import os

class GitRepo(object):

    def __init__(self, path):
        self.path = path
        self.devnull = open(os.devnull, 'w')

    def get_config(self, key):
        proc = subprocess.Popen(["git", "config", key], stdout=subprocess.PIPE, cwd=self.path)
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
        proc = subprocess.Popen(["git", "symbolic-ref", name], stdout=subprocess.PIPE)
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
