'''Global engine scope'''
__version__ = '0.1.0'

import e3d3.log as log
import e3d3.error as error
import e3d3.events as events
import e3d3.core as core
import e3d3.math as math
import e3d3.data as data


def expose(target):
    globals()[target.__name__] = target
    return target
