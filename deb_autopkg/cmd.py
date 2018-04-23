from builder import Builder
from conf import load

def build_pool(conffile, pool):
    return Builder(load(conffile)).build_pool(pool)

def upload_pool(conffile, pool):
    return Builder(load(conffile)).upload_pool(pool)

def build_all(conffile):
    return Builder(load(conffile)).build_all()

def build_package(conffile, pkg):
    return Builder(load(conffile)).build_package(pkg)

def clone_all(conffile):
    return Builder(load(conffile)).clone_all()
