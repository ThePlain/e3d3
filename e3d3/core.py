# pylint: disable=global-statement
'''Core application module
    Main loop an manager of all application systems
'''


import e3d3
import e3d3.log
import e3d3.data
import e3d3.error
import e3d3.events


logger = e3d3.log.get(__name__)


SYSTEMS = dict()
IS_RUN = False


class Component:
    '''Base class of all Components
    Automatic all child classes expose to e3d3 scope
    '''

    def __init_subclass__(cls):
        super().__init_subclass__()
        e3d3.expose(cls)
        Components[cls.__name__] = cls
        logger.debug('%s - registered', cls.__name__)

    def __init__(self, entity):
        self.entity = entity


class Components(e3d3.data.ContentManager):
    @classmethod
    def setitem(cls, key, value):
        cls.heap[key] = value

    @classmethod
    def getitem(cls, key):
        return cls.heap[key]


class System:
    '''Base class of all Systems
    Automatic all child classes expose to e3d3 scope and register in system list

    All method require @staticmethod or @classmethod decorator because system is a singletone
    '''

    order = 0

    def __init_subclass__(cls):
        super().__init_subclass__()
        e3d3.expose(cls)
        Systems[cls.__name__] = cls
        SYSTEMS[cls.__name__] = cls
        logger.debug('%s - registered.', cls.__name__)

    @classmethod
    def run(cls):
        '''Base interface of a system
        Called on application start
        '''

    @classmethod
    def update(cls):
        '''Base interface of a system
        Called every update in main loop
        '''

    @classmethod
    def clean(cls):
        '''Base interface of a system
        Called on application stop
        '''


class Systems(e3d3.data.ContentManager):
    @classmethod
    def setitem(cls, key, value):
        cls.heap[key] = value

    @classmethod
    def getitem(cls, key):
        return cls.heap[key]



def sorted_systems():
    '''Return sorted iterator of all systems by order'''
    global SYSTEMS

    def sort(system: System):
        return system.order

    return sorted(SYSTEMS.values(), key=sort)


def run():
    '''Engine entry point'''

    global IS_RUN

    config = e3d3.data.Config.load('e3d3.yaml')

    IS_RUN = True

    logger.info('Application start')

    for module in config['modules']:
        __import__(module)

    e3d3.events.subscribe(clean, 'app.stop')
    e3d3.events.dispatch('app.run')
    for system in sorted_systems():
        system.run()

    while IS_RUN:
        e3d3.events.dispatch('app.update.before')
        for system in sorted_systems():
            system.update()
        e3d3.events.dispatch('app.update')

    e3d3.events.dispatch('app.stop')


def clean():
    '''Engine cleaning function
    For execute dispath 'app.stop' event
    '''
    global IS_RUN
    global config

    IS_RUN = False

    e3d3.events.dispatch('app.clean')
    for system in sorted_systems():
        system.clean()

    logger.info('Application stop')
