import json
import os

import six

from file_cache import CACHE_DIR, CacheBase


class FileCache(CacheBase):
    type = 'file'

    def get_cache_path(self, name, ext='json'):
        name = str(name)
        return os.path.join(self.get_and_create_cache_dir(), '.'.join([name, ext]))

    def save(self, data, name, ext='json'):
        file = self.get_cache_path(name, ext)
        if not isinstance(data, six.string_types) and ext == 'json':
            data = json.dumps(data)
        elif not isinstance(data, six.string_types) and ext == 'xml':
            from lxml import etree
            data = etree.tostring(data)
            data = data.decode('utf-8')
        with open(file, 'w') as f:
            f.write(data)

    def load(self, name, ext='json'):
        name = str(name)
        file = self.get_cache_path(name, ext)
        if not os.path.lexists(file):
            return
        if ext == 'json':
            return json.load(open(file))
        elif ext == 'xml':
            from lxml import etree
            return etree.fromstring(open(file).read())
        else:
            return open(file).read()
