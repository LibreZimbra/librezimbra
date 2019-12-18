
"""Target configuration"""
class TargetSpec(object):

    """[private]"""
    def __init__(self, name, pool):
        self.name = name
        self.pool = pool

    def get_target_name(self):
        return self.name

    def get_pool_name(self):
        if self.pool is None:
            return 'global'
        else:
            return self.pool.name

    def get_aptrepo_path(self):
        if self.pool is None:
            return None
        else:
            return self.pool.get_aptrepo_path()
