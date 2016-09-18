import os

__version__ = '0.1.0'
CACHE_DIR = os.path.expanduser('~/.local/cache')


class CacheBase(object):
    type = None

    def __init__(self, project_name):
        self.project_name = project_name

    def get_cache_dir(self):
        return os.path.join(CACHE_DIR, self.project_name, self.type)

