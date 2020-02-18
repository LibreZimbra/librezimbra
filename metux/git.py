from subprocess import call, Popen, PIPE
from os import devnull, environ
from os.path import abspath, isfile
from copy import deepcopy
from uuid import uuid1
from metux import mkdir, rmtree

_devnull = open(devnull, 'w')

class GitRepo(object):

    def __init__(self, path):
        self.path       = abspath(path)
        self.gitdir     = self.path+"/.git"
        self.gitcmd     = [ 'git' ]

    def _gitcall(self, args, index_file=None, work_tree=None, quiet=0):
        e = deepcopy(environ)

        if index_file is not None:
            e['GIT_INDEX_FILE'] = index_file
        if work_tree is not None:
            e['GIT_WORK_TREE']  = work_tree

        if quiet:
            return (call(self.gitcmd + args, cwd=self.path, stdout=_devnull, env=e)==0)
        else:
            return (call(self.gitcmd + args, cwd=self.path, env=e)==0)

    def _gitout(self, args, index_file=None, work_tree=None):
        e = deepcopy(environ)

        if index_file is not None:
            e['GIT_INDEX_FILE'] = index_file
        if work_tree is not None:
            e['GIT_WORK_TREE']  = work_tree

        proc = Popen(self.gitcmd + args, stdout=PIPE, cwd=self.path, env=e)
        (out, err) = proc.communicate()
        return out.strip()

    def get_config(self, key):
        return self._gitout(["config", key])

    def set_config(self, key, value):
        if self.get_config(key) == value:
            return False
        else:
            self._gitcall(['config', key, value])
            return True

    def initialize(self):
        mkdir(self.path)
        if (isfile(self.gitdir+'/config') and isfile(self.gitdir+'/HEAD')):
            return False
        return self._gitcall(['init', self.path])

    def set_remote(self, name, url):
        # need to do that complicated to defeat shortcut evaluation
        a = self.set_config('remote.'+name+'.url', url)
        b = self.set_config('remote.'+name+'.fetch', '+refs/heads/*:refs/remotes/'+name+'/*')
        if (a or b):
            return self._gitcall(['remote', 'update', name])

    def get_symbolic_ref(self, name):
        return self._gitout(["symbolic-ref", name])

    def is_checked_out(self):
        return self._gitcall(['rev-parse', '--quiet', '--verify', 'HEAD'], quiet=1)

    def is_branch(self, branch):
        return self.is_ref('refs/heads/'+branch)

    def is_ref(self, refname):
        return self._gitcall(['show-ref', '--verify', '--quiet', refname])

    def checkout(self, ref, branch):
        return self._gitcall(['checkout', ref, '-b', branch])

    def load_index(self, workdir, indexfile):
        return self._gitcall(['add', '-A'], index_file=indexfile, work_tree=workdir)

    def checkout_index(self, workdir, indexfile):
        return self._gitcall(['checkout-index', '-a'], index_file=indexfile, work_tree=workdir)

    def read_tree(self, indexfile, treeish):
        return self._gitcall(['read-tree', treeish], index_file=indexfile)

    def write_tree(self, indexfile):
        return self._gitout(['write-tree'], index_file=indexfile)

    def commit_tree(self, treeish, msg, parent = None):
        args = ['commit-tree', treeish, '-m', msg]
        if parent is not None:
            args += ['-p', parent]
        return self._gitout(args)

    def create_branch(self, branch, treeish):
        return self._gitcall(['branch', branch, treeish])

    def remove_branch(self, branch):
        return self._gitcall(['update-ref', '-d', 'refs/heads/'+branch])

    """extract a treeish into separate workdir"""
    def extract_tree(self, workdir, treeish):
        tmpindex = self.get_tmpindex()
        ret = self.read_tree(tmpindex, treeish) and self.checkout_index(workdir, tmpindex)
        rmtree(tmpindex)
        return ret

    """import a tree into a new branch, as initial commit"""
    def import_initial_tree(self, tree, branch, msg, parent = None):
        temp_index = self.get_tmpindex()
        if self.load_index(tree, temp_index):
            treeish = self.write_tree(temp_index)
            commit = self.commit_tree(treeish, msg, parent)
            ret = self.create_branch(branch, commit)
        else:
            ret = False
        rmtree(temp_index)
        return ret

    def get_tmpdir(self):
        tmp = abspath(self.gitdir+'/tmp/'+str(uuid1()))
        mkdir(tmp)
        return tmp

    def get_tmpindex(self):
        return abspath(self.gitdir+'/'+str(uuid1())+'.index')

    def submodule_init(self):
        return self._gitcall(['submodule', 'update', '--init', '--recursive'])

    def archive(self, ref = 'HEAD', output = None, prefix = None, format = None):
        args = ['archive']
        if format is not None:
            args += ['--format', format]
        if prefix is not None:
            args += ['--prefix', prefix]
        if output is not None:
            args += ['--output', output]
        args += [ref]

        return self._gitcall(args)

    def get_head_commit(self):
        args = [ 'rev-parse', '--verify', 'HEAD^{commit}' ]
        return self._gitout(args)
