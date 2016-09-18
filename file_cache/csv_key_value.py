import csv
import datetime
import hashlib
import os

from file_cache import CacheBase


class KeyValuesCache(CacheBase):
    def __init__(self, project_name, fields=('name', 'value', 'updated_at'), dialect='excel-tav'):
        super(KeyValuesCache, self).__init__(project_name)
        self.fields = fields
        self.dialect = dialect

    def get_cache_path(self, key):
        hash = hashlib.md5(key.encode('utf-8')).hexdigest()[:2]
        return os.path.join(self.get_cache_dir(), '{}.csv'.format(hash))

    def _get_csv_reader(self, key):
        return csv.DictReader(open(self.get_cache_path(key)), fieldnames=self.fields, dialect=self.dialect)

    def _save_cache(self, path, lines):
        f = open(path, 'w')
        d = csv.DictWriter(f, fieldnames=self.fields, dialect=self.dialect)
        d.writerows(lines)
        f.close()

    def cache_line(self, key, value=None, **kwargs):
        data = {'key': key}
        if 'value' in self.fields:
            data['value'] = value
        if 'updated_at' in self.fields:
            data['updated_at'] = datetime.datetime.now()
        data.update(kwargs)
        return data

    def save(self, key, value=None, **kwargs):
        path = self.get_cache_path(key)
        lines = list(self._get_csv_reader(key)) if os.path.lexists(path) else []
        new_line = self.cache_line(key, value, **kwargs)
        for i, line in enumerate(lines):
            if not line['key'] == key:
                continue
            lines[i] = new_line
            return self._save_cache(path, lines)
        lines.append(new_line)
        self._save_cache(path, lines)

    def load(self, key, label):
        path = self.get_cache_path(key)
        lines = list(self._get_csv_reader(key)) if os.path.lexists(path) else []
        for line in lines:
            if line['name'] == key:
                return line
