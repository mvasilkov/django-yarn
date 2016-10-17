from collections import OrderedDict
import os.path

from django.conf import settings
from django.contrib.staticfiles.finders import FileSystemFinder
from django.core.files.storage import FileSystemStorage

_DEFAULTS = {
    'ROOT_PATH': '.',
    'STATIC_FILES_PREFIX': '',
}


def _setting(name):
    return getattr(settings, 'YARN_%s' % name, _DEFAULTS[name])


class YarnFinder(FileSystemFinder):
    def __init__(self, app_names=None, *args, **kwargs):
        self.destination = _setting('STATIC_FILES_PREFIX')
        self.node_modules_path = os.path.join(_setting('ROOT_PATH'), 'node_modules')

        self.locations = [(self.destination, self.node_modules_path)]
        self.storages = OrderedDict()

        filesystem_storage = FileSystemStorage(location=self.locations[0][1])
        filesystem_storage.prefix = self.locations[0][0]
        self.storages[self.locations[0][1]] = filesystem_storage
