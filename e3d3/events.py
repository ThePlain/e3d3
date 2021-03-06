import weakref


LISTENERS = dict()
LASYQUEUE = list()
# TODO: Strong holder with weak link to item


def subscribe(target, *events):
    for event in events:
        if event not in LISTENERS:
            LISTENERS[event] = weakref.WeakSet()
        LISTENERS[event].add(target)
    return LISTENERS[events[0]]


def select(event):
    if event in LISTENERS:
        return LISTENERS[event]
    return []


def dispatch(event, *args, **kwargs):
    if event not in LISTENERS:
        return

    for listener in LISTENERS[event]:
        listener(*args, **kwargs)


def lazy_distpatch(event, *args, **kwargs):
    global LASYQUEUE

    LASYQUEUE.append((event, args, kwargs))


def exec_lasyqueue():
    global LASYQUEUE

    if not LASYQUEUE:
        return

    queue = LASYQUEUE
    LASYQUEUE = list()

    for task in queue:
        name, args, kwargs = task
        dispatch(name, *args, **kwargs)


def lookup(target):
    events = []
    for name, listeners in LISTENERS.items():
        if target in listeners:
            events.append(name)
    return events


def remove(target, *events):
    for event in events:
        if event in LISTENERS:
            LISTENERS[events].remove(target)


def clean(*events):
    for event in events:
        if event in events:
            del LISTENERS[event]
