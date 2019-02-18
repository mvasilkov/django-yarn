from collections import OrderedDict
import os
import os.path
import sys

from django.conf import settings
from django.contrib.staticfiles.finders import FileSystemFinder
from django.contrib.staticfiles.utils import matches_patterns
from django.core.files.storage import FileSystemStorage

_DEFAULTS = {
    'ALLOW_FILES': any,
    'ROOT_PATH': '.',
    'STATIC_FILES_PREFIX': '',
}


def _setting(name):
    return getattr(settings, 'YARN_%s' % name,
                   getattr(settings, 'NPM_%s' % name, _DEFAULTS[name]))


class YarnFinder(FileSystemFinder):
    def __init__(self, app_names=None, *args, **kwargs):
        self.allow_files = _setting('ALLOW_FILES')
        self.destination = _setting('STATIC_FILES_PREFIX')
        self.node_modules_path = os.path.join(_setting('ROOT_PATH'), 'node_modules')

        self.locations = [(self.destination, self.node_modules_path)]
        self.storages = OrderedDict()

        for prefix, root in self.locations:
            filesystem_storage = FileSystemStorage(location=root)
            filesystem_storage.prefix = prefix
            self.storages[root] = filesystem_storage

    def find_location(self, root, path, prefix=None):
        if prefix:
            prefix += os.sep
            if not path.startswith(prefix):
                return None
            path = path[len(prefix):]

        if self.allow_files is not any and not matches_patterns(path, self.allow_files):
            return None

        return super().find_location(root, path)

    def list(self, ignore_patterns):
        gen = super().list(ignore_patterns)

        if self.allow_files is any:
            yield from gen
            return

        for path, storage in gen:
            if matches_patterns(path, self.allow_files):
                yield path, storage


def _initialize():
    global matches_patterns

    if not sys.platform.startswith('win') or matches_patterns.__name__ == 'subst':
        return

    _matches_patterns = matches_patterns

    def subst(path, patterns=None):
        return _matches_patterns(path.replace(os.sep, '/'), patterns)

    matches_patterns = subst


_initialize()
