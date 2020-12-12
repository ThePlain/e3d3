import enum
import weakref

import e3d3
import e3d3.log
import e3d3.math


logger = e3d3.log.get(__name__)


class DispatchMode(enum.Enum):
    UP: 'UP'
    DOWN: 'DOWN'
    SINGLE: 'SINGLE'
    BROADCAST: 'BROADCAST'


class Transform:
    def __init__(self, entity):
        self.__location = e3d3.math.Vector()
        self.__rotation = e3d3.math.Quaternion()
        self.__scale = e3d3.math.Vector(1, 1, 1)
        self.__local = e3d3.math.Matrix()
        self.__world = e3d3.math.Matrix()
        self.__entity = entity
        self.dirty = False

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value):
        self.__location = value
        self.dirty = True

    @property
    def rotation(self):
        return self.__rotation

    @rotation.setter
    def rotation(self, value):
        self.__rotation = value
        self.dirty = True

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, value):
        self.__scale = value
        self.dirty = True

    @property
    def local(self):
        return self.__local

    @property
    def world(self):
        return self.__world

    def transform(self):
        if self.dirty:
            self.dirty = True

            self.__local = e3d3.math.Matrix.from_components(
                self.__location,
                self.__rotation,
                self.__scale,
            )

            if self.__entity.parent:
                self.__world = self.__entity.parent.transform.world * self.__local
            else:
                self.__world = self.__local.copy


class Node:
    root = None

    @classmethod
    def create_root(cls):
        node = cls('root:', None)
        cls.root = node

    def __init__(self, name, parent = None):
        self.__name = name
        self.__parent = None
        self.__childs = dict()
        self.__transform = Transform(self)
        self.__components = dict()

        if parent:
            self.parent = parent

        e3d3.events.subscribe(self.__transform.transform, 'app.update.before')

    @property
    def weak(self):
        return weakref.ref(self)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if self.__parent:
            del self.__parent.childs[self.__name]
            self.__parent.childs[value] = self

        self.__name = value

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__transform.dirty = True

        if self.__parent:
            del self.__parent.childs[self.__name]

        if value:
            self.__parent = value.weak
            self.__parent.childs[self.__name] = self
            e3d3.events.dispatch('graph.attach', self.weak)

        else:
            self.__parent = None

    @property
    def childs(self):
        return self.__childs

    @property
    def transform(self):
        return self.__transform

    @property
    def components(self):
        return self.__components

    def find_component(self, name):
        return self.__components.get(name, None)

    def add_component(self, name):
        component = e3d3.data.Components[name]
        instance = component(self.weak)
        self.__components[name] = instance
        instance.message('on_awake')

        if e3d3.core.IS_RUN:
            instance.message('on_start')

    def remove_component(self, name):
        instance = self.find_component(name)
        if instance:
            instance.message(name, 'on_remove')
            del self.__components[name]

    def find_node(self, path):
        names = path.split('/')
        current = self

        for num, name in enumerate(names):
            if name == 'root:':
                if num != 0:
                    raise e3d3.error.GraphError('bad path format: "root:" require place at start.')

                if Node.root is None:
                    raise e3d3.error.GraphError('Root node is not attached.')

                current = Node.root.weak

            if name in ('.', ''):
                continue

            if name == '..':
                if current.parent:
                    return None

                current = current.parent

            if name in current.childs:
                current = current.childs[name]

            else:
                return None

        return current

    def add_node(self, fullpath):
        node = self.find_node(fullpath)

        if node:
            raise e3d3.error.GraphError(f'node already exists: {fullpath}.')

        path, name = fullpath.rsplit('/')
        parent = self.find_node(path)

        if path and not parent:
            raise e3d3.error.GraphError(f'parent node not found: {path}')

        node = Node(name, parent)

    def remove_node(self, path):
        node = self.find_node(path)

        if node and node.parent:
            node.cast(DispatchMode.DOWN, 'on_delete')
            node.parent = None

    def move_node(self, path):
        parent = self.find_node(path)

        if not parent:
            raise e3d3.error.GraphError(f'parent node not found: {path}')

        self.parent = parent

    def message(self, mode, name, *args, **kwargs):
        if mode in (DispatchMode.BROADCAST, DispatchMode.UP):
            for child in self.childs.values():
                child.message(DispatchMode.UP, name, *args, **kwargs)

        for component in self.components.values():
            component.message(name, *args, **kwargs)

        if mode in (DispatchMode.BROADCAST, DispatchMode.UP):
            if self.__parent:
                self.__parent.message(DispatchMode.UP, name, *args, **kwargs)
