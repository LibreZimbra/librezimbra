# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

from subprocess import call
from os import makedirs
from os.path import abspath
import errno

def mkdir(dirname):
    try:
        makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        # time.sleep might help here
        pass

def rmtree(dirname):
    call(['rm', '-Rf', abspath(dirname)])
