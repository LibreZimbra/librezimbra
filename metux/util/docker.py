from subprocess import Popen, PIPE, check_output
from os import environ
import atexit

class DockerContainer:
    def __init__(self, docker, id):
        self.my_docker = docker
        self.my_id = id
        atexit.register(self.__atexit)

    def _call_stdout(self, cmd, args = []):
        return self.my_docker._call_stdout([cmd, self.my_id]+args)

    def _call_direct(self, cmd, args = []):
        return self.my_docker._call_direct([cmd, self.my_id]+args)

    def start(self):
        return self._call_stdout('start')

    def stop(self):
        return self._call_catch('stop')

    def remove(self):
        return self._call_catch('rm')

    def destroy(self):
        return self.my_docker._call_catch(['rm', '-f', self.my_id])

    def execute(self, args):
        return self._call_direct('exec', args)

    def exec_stdout(self, args):
        return self.my_docker._call_stdout(['exec', self.my_id]+args)

    def exec_catch(self, args):
        return self.my_docker._call_catch(['exec', self.my_id]+args)

    def mkdirs(self, dirs):
        return self.execute(['mkdir', '-p']+dirs)

    def cp_to(self, src, dest, owner=None, mode=None):
        ret = self.my_docker._call_direct(['cp', src, self.my_id+':'+dest])
        if owner is not None:
            self.chown(owner, [dest])
        if mode is not None:
            self.chmod(mode, [dest])
        return ret

    def cp_from(self, src, dest):
        return self.my_docker._call_direct(['cp', self.my_id+':'+src, dest])

    def chown(self, owner, files):
        return self.my_docker._call_direct(['exec', self.my_id, 'chown', owner]+files)

    def chmod(self, mode, files):
        return self.my_docker._call_direct(['exec', self.my_id, 'chmod', mode]+files)

    def rm_recursive(self, dirs):
        return self.my_docker._call_direct(['exec', self.my_id, 'rm', '-Rf']+dirs)

    def __atexit(self):
        self.destroy()

class Docker:
    def __init__(self):
        if 'DOCKER' in environ:
            self.cmd = environ['DOCKER']
        else:
            self.cmd = 'docker'

    def _call_stdout(self, args):
        return check_output([self.cmd]+args)

    def _call_direct(self, args):
        process = Popen([self.cmd]+args)
        stdout, stderr = process.communicate()
        return process.wait()

    def _call_catch(self, args):
        process = Popen([self.cmd]+args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        exit_code = process.wait()
        return exit_code, stdout, stderr

    def container_create(self, image, args):
        return DockerContainer(self, self._call_stdout(['create', image]+args).strip())

    def container_qrun(self, image, cmdline, extra_args=[], env={}):
        if image is None:
            raise Exception("image cant be none")

        env_param = []
        for n,v in env.iteritems():
            env_param.append('-e')
            env_param.append(n+'='+v)

        x = ['run', '-ti', '--rm']+ env_param + extra_args + [image] + cmdline
        return self._call_direct(x)

    def image_import(self, filename, name):
        return self._call_stdout(['image', 'import', filename, name])
