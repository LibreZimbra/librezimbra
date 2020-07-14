from subprocess import call
from os.path import abspath

def mkdir(dirname):
    call(['mkdir', '-p', abspath(dirname)])

def rmtree(dirname):
    call(['rm', '-Rf', abspath(dirname)])
