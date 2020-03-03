from subprocess import call
from ..conf.err import ConfigFail

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

    raise ConfigFail("unknown upload protocol: %s" % param['protocol'])
