from builder import Builder
from conf import load

def build_pool(conffile, pool):
    return Builder(load(conffile)).build_pool(pool)

def upload_pool(conffile, pool):
    return Builder(load(conffile)).upload_pool(pool)

def deploy_pool(conffile, pool):
    return Builder(load(conffile)).deploy_pool(pool)

def build_all(conffile):
    return Builder(load(conffile)).build_all()

def build_package(conffile, pkg):
    return Builder(load(conffile)).build_package(pkg)

def clone_all(conffile):
    return Builder(load(conffile)).clone_all()

def get_dut(conffile, name):
    return load(conffile).get_dut(name)

def dut_exec(conffile, dutname, cmd = []):
    return get_dut(conffile, dutname).dut_exec(cmd)
