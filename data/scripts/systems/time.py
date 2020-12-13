import time
import weakref

import e3d3
import e3d3.core


class Timer:
    __slots__ = ('callback', 'nextcall', 'timeout', 'repeat')

    def __init__(self, callback, timeout, repeat=False):
        self.callback = weakref.ref(callback)
        self.timeout = timeout
        self.nextcall = Time.current + self.timeout
        self.repeat = repeat

    def dispatch(self):
        self.callback()
        if not self.repeat:
            Time.remove(self)


class Time(e3d3.core.System):
    current = 0
    system = 0
    delta = 0
    timers = []

    @classmethod
    def run(cls):
        cls.system = time.time()

    @classmethod
    def update(cls):
        system = time.time()
        cls.delta = system - cls.system
        cls.current += cls.delta
        cls.system = system

        for timer in filter(cls.filter, cls.timers):
            timer.dispatch()

    @classmethod
    def filter(cls, item):
        return item.nextcall <= cls.current

    @classmethod
    def remove(cls, timer):
        cls.timers.remove(timer)

    @classmethod
    def timeout(cls, callback, timeout):
        timer = Timer(callback, timeout, False)
        cls.timers.append(timer)
        return timer

    @classmethod
    def interval(cls, callback, timeout):
        timer = Timer(callback, timeout, True)
        cls.timers.append(timer)
        return timer
