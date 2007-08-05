'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

import weakref
import threading


def chop(s, n=1):
    '''Chops n words from s string and returns a list.

    Returned list:
    [w1, w2, ..., wn, rest_of_string]
    '''

    spl = s.split()
    res = []
    while len(res) < n:
        if len(spl) == 0:
            raise ValueError('chop: Could not chop %d words from \'%s\'' % (n, s))
        if spl[0]:
            res.append(spl[0])
        del spl[0]
    res.append(type(s)(' ').join(spl))
    return res


def quote(s):
    ''' Adds quotes to string if neede.

    If s contains spaces, returns the string in quotes (if it contained quotes too, they are
    replaced by \". If string doesn't contain spaces, returns the string unchanged.
    '''

    if ' ' in s:
        return '"%s"' % s.replace('"', '\\"')
    return s


def esplit(s, d=None):
    if s:
        return s.split(d)
    return []


def EventHandling(events):
    ''' Creates and returns a new EventHandling class.

    Parameters:
        events
            list of events names

    Returned class:
        Properties:
            On..., where '...' is one of 'events'
                allow assigning of an event handler (callable) to an event,
                None by default

        Metods:
            _RegisterEventHandler(name, info, target)
                registers a callable as event handler, any number of callables can be
                assigned to an event
                name - event name
                info - unique string defining this handler, 'On...' properties use 'default',
                       if None, a unique value will be generated, it will also be returned for
                       future use with _UnregisterEventHandler()
                target - callable, event handler

            _UnregisterEventHandler(name, info)
                unregisteres an event handler
                name - event name
                info - same as with _RegisterEventHandler()

            _RegisterEventsClass(cls)
                registers a class as event handler, class should contain methods with names
                corresponding to event names, class will be instatinated automatically
                cls - class to register

            _UnregisterEventsClass(cls)
                unregisteres a class
                cls - class to unregister

            _CallEventHandler(name, ...)
                calls all event handlers defined for given event (name), additional parameters
                will be passed unchanged to event handlers, all event handlers are fired on
                separate threads
                name - event name
                ... - event handlers parameters
    '''

    class EventHandlingBase(object):
        def __init__(self):
            self._Events = {}
            self._EventHandlers = {}

        def _CallEventHandler(self, name, *args, **kwargs):
            for h in self._EventHandlers.get(name, {}).values():
                t = threading.Thread(name=name, target=h, args=args, kwargs=kwargs)
                t.setDaemon(False)
                t.start()
            for h in self._Events.values():
                if hasattr(h, name):
                    t = threading.Thread(name=name, target=getattr(h, name), args=args, kwargs=kwargs)
                    t.setDaemon(False)
                    t.start()

        def _GetEventHandler(self, name):
            try:
                return self._EventHandlers.get(name, {})['default']
            except KeyError:
                return None

        def _SetEventHandler(self, name, target):
            if target:
                self._RegisterEventHandler(name, 'default', target)
            else:
                self._UnregisterEventHandler(name, 'default')

        def _RegisterEventHandler(self, name, info, target):
            if not callable(target):
                raise ValueError('%s is not callable' % repr(target))
            if not info:
                info = self._CreateEventHandlerInfo(name)
            if name not in self._EventHandlers:
                self._EventHandlers[name] = {}
            self._EventHandlers[name][info] = target
            return info

        def _UnregisterEventHandler(self, name, info):
            try:
                del self._EventHandlers.get(name, {})[info]
            except KeyError:
                pass

        def _RegisterEvents(self, info, obj):
            self._Events[info] = obj

        def _UnregisterEvents(self, info):
            try:
                del self._Events[info]
            except KeyError:
                pass

        def _CreateEventHandlerInfo(self, name):
            i = 1
            while str(i) in self._EventHandlers.get(name, {}):
                i += 1
            return str(i)

    def make_event(event):
        return property(lambda self: self._GetEventHandler(event), lambda self, value: self._SetEventHandler(event, value))

    for event in events:
        setattr(EventHandlingBase, 'On' + event, make_event(event))
    return EventHandlingBase


class Cached(object):
    ''' Base class for cached objects.

    Every object is identified by an Id. Trying to create two objects with same Id yields
    the same object.
    '''
    _cache_ = weakref.WeakValueDictionary()

    def __new__(cls, Id, *args, **kwargs):
        h = cls, Id
        try:
            return cls._cache_[h]
        except KeyError:
            o = object.__new__(cls)
            if hasattr(o, '_Init'):
                o._Init(Id, *args, **kwargs)
            cls._cache_[h] = o
            return o
