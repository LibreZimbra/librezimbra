__all__ = [ "targetspec", "poolspec", "pkgspec", "config" ]

from .targetspec import TargetSpec
from .poolspec import PoolSpec
from .pkgspec import PkgSpec
from .config import Config

"""create new global config object and load config file"""
def load(fn):
    cf = Config()
    cf.load(fn)
    return cf
