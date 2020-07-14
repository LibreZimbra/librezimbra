# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

from subprocess import call
from metux.util.specobject import SpecError

def rsync_ssh(username, hostname, source, path):
    return (call([
        'rsync',
        '--progress',
        '--rsh=ssh',
        '-r',
        source+"/",
        username+"@"+hostname+":/"+path ]) == 0)

def run_upload(param):
    if param['protocol'] == 'rsync+ssh':
        return rsync_ssh(param['username'], param['hostname'], param['source'], param['path']);

    raise SpecError("unknown upload protocol: %s" % param['protocol'])
