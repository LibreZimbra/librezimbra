from subprocess import call
from os.path import abspath
from os import path, chmod
import os
import stat

def mkdir(dirname):
    call(['mkdir', '-p', abspath(dirname)])

def rmtree(dirname):
    call(['rm', '-Rf', abspath(dirname)])

def extract_tar(tarball, tempdir):
    tarball = abspath(tarball)
    tempdir = abspath(tempdir)
    rmtree(tempdir)
    mkdir(tempdir)

    if (tarball.endswith(".tar.gz")):
        return call(['tar', '-xzf', abspath(tarball), '-C', tempdir])
    elif (tarball.endswith(".tar")):
        return call(['tar', '-xf', abspath(tarball), '-C', tempdir])
    elif (tarball.endswith(".tar.bz2")):
        return call(['tar', '-xjf', abspath(tarball), '-C', tempdir])
    elif (tarball.endswith(".zip")):
        return call(['unzip', abspath(tarball), '-d', tempdir])
    else:
        raise BaseException("unknown format: "+tarball)

def write_file(fn, text):
    mkdir(path.dirname(fn))
    with open(fn, "w") as f:
        f.write(text)

def setexec(fn):
    chmod(fn, os.stat(fn).st_mode | stat.S_IEXEC)
