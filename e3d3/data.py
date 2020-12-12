import os
import sys
import yaml

import e3d3
import e3d3.log
import e3d3.error
import e3d3.events


logger = e3d3.log.get(__name__)


WORKDIR = os.getcwd()
DATADIR = os.path.join(WORKDIR, 'data')
STDLIBS = os.path.join(DATADIR, 'stdlib')

sys.path.append(DATADIR)
sys.path.append(STDLIBS)


class ContentManagerMeta(type):
    def __getitem__(cls, key):
        return cls.getitem(key)

    def __setitem__(cls, key, value):
        cls.setitem(key, value)

    def __delitem__(cls, key):
        cls.delitem(key)

    def __iter__(cls):
        return cls.iter()


class ContentManager(metaclass=ContentManagerMeta):
    heap = dict()

    def __init_subclass__(cls):
        super().__init_subclass__()

        if cls.__name__ not in globals():
            globals()[cls.__name__] = cls

        logger.debug('Register new content manager: %s', cls.__name__)

    @classmethod
    def getitem(cls, key):
        return cls.heap[key]

    @classmethod
    def setitem(cls, key, value):
        cls.heap[key] = value

    @classmethod
    def delitem(cls, key, value):
        del cls.heap[key]

    @classmethod
    def iter(cls):
        return iter(cls.heap.items())

    @classmethod
    def save(cls, path):
        raise e3d3.error.DataError(f'{cls.__name__} does not support or not implement save.')

    @classmethod
    def load(cls, path):
        raise e3d3.error.DataError(f'{cls.__name__} does not support or not implement load.')

    @classmethod
    def new(cls, path):
        raise e3d3.error.DataError(f'{cls.__name__} does not support or not implement new.')


class Config(ContentManager):
    @classmethod
    def load(cls, path):
        fullpath = os.path.join(DATADIR, path)

        if not os.path.isfile(fullpath):
            raise e3d3.error.DataError(f'cant find resource: {fullpath}')

        with open(fullpath, 'r') as stream:
            cls.heap[path] = yaml.safe_load(stream)

        return cls.heap[path]