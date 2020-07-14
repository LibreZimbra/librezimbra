# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

from subprocess import call
from os.path import abspath

def mkdir(dirname):
    call(['mkdir', '-p', abspath(dirname)])

def rmtree(dirname):
    call(['rm', '-Rf', abspath(dirname)])
