'''
Utility functions and classes used internally by Skype4Py.
'''

import sys
import weakref
import threading
from new import instancemethod


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
    '''Adds quotes to string if needed.

    If s contains spaces, returns the string in quotes (if it contained quotes too, they are
    preceded with backslash. If string doesn't contain spaces, returns the string unchanged.
    '''

    if ' ' in s:
        return '"%s"' % s.replace('"', '\\"')
    return s


def esplit(s, d=None):
    '''Like s.split(d) but for empty strings returns empty list instead of [''].
    '''

    if s:
        return s.split(d)
    return []


def deprecated(klass, attrold, attrnew):
    '''Prints a deprecation note to sys.stderr.
    '''

    print >>sys.stderr, 'Skype4Py warning!', klass + '.' + attrold, 'is deprecated, use', klass + '.' + attrnew, 'instead!'


class _WeakMethod(object):
    '''Helper class for WeakCallableRef function (see below).
    Don't use directly.
    '''

    def __init__(self, method, callback=None):
        self.im_func = method.im_func
        try:
            self.weak_im_self = weakref.ref(method.im_self, self._dies)
        except TypeError:
            self.weak_im_self = None
        self.im_class = method.im_class
        self.callback = callback

    def _dies(self, ref):
        self.im_func = self.im_class = None
        if self.callback != None:
            self.callback(self)

    def __call__(self):
        if self.weak_im_self:
            im_self = self.weak_im_self()
            if im_self == None:
                return None
        else:
            im_self = None
        return instancemethod(self.im_func, im_self, self.im_class)


def WeakCallableRef(c, callback=None):
    '''Creates and returns a new weak reference to a callable object.

    In contrast to weakref.ref() works on all kinds of callables.
    Parameters are same as for weakref.ref().
    '''

    try:
        return _WeakMethod(c, callback)
    except AttributeError:
        return weakref.ref(c, callback)


class _EventHandlingThread(threading.Thread):
    def __init__(self, name=None):
        threading.Thread.__init__(self, name='%s event handler' % name)
        self.setDaemon(False)
        self.lock = threading.Lock()
        self.queue = []

    def enqueue(self, target, args, kwargs):
        self.queue.append((target, args, kwargs))

    def run(self):
        while True:
            try:
                self.lock.acquire()
                h = self.queue[0]
                del self.queue[0]
            except IndexError:
                break
            finally:
                self.lock.release()
            h[0](*h[1], **h[2])

class EventHandlingBase(object):
    '''Class used as a base by all classes implementing event handlers.'''

    def __init__(self):
        '''Initializes the object.'''
        self._EventHandlerObj = None
        self._DefaultEventHandlers = {}
        self._EventHandlers = {}
        self._EventThreads = {}

    def _CallEventHandler(self, Event, *args, **kwargs):
        '''Calls all event handlers defined for given Event (str), additional parameters
        will be passed unchanged to event handlers, all event handlers are fired on
        separate threads.
        '''

        # get list of relevant handlers
        allhandlers = [x() for x in self._EventHandlers.get(Event, [])]
        handlers = filter(bool, allhandlers)
        if len(allhandlers) != len(handlers):
            # cleanup
            self._EventHandlers[Event] = [x for x in self._EventHandlers[Event] if x()]
        try:
            h = self._DefaultEventHandlers[Event]()
            if h:
                handlers.append(h)
        except KeyError:
            pass
        try:
            handlers.append(getattr(self._EventHandlerObj, Event))
        except AttributeError:
            pass
        # if no handlers, leave
        if not handlers:
            return
        # initialize event handling thread if needed
        if Event in self._EventThreads:
            t = self._EventThreads[Event]
            t.lock.acquire()
            if not self._EventThreads[Event].isAlive():
                t = self._EventThreads[Event] = _EventHandlingThread(Event)
        else:
            t = self._EventThreads[Event] = _EventHandlingThread(Event)
        # enqueue handlers in thread
        for h in handlers:
            t.enqueue(h, args, kwargs)
        # start serial event processing
        try:
            t.lock.release()
        except:
            t.start()

    def RegisterEventHandler(self, Event, Target):
        '''Registers an event handler.

        @param Event: Name of the event.
        @type Event: str
        @param Target: Callable to register as the event handler.
        @type Target: callable
        @return: Always True.
        @rtype: bool
        '''

        if not callable(Target):
            raise TypeError('%s is not callable' % repr(Target))
        if Event not in self._EventHandlers:
            self._EventHandlers[Event] = []
        self._EventHandlers[Event].append(WeakCallableRef(Target))
        return True

    def UnregisterEventHandler(self, Event, Target):
        '''Unregisters an event handler.

        @param Event: Name of the event.
        @type Event: str
        @param Target: Callable to unregister.
        @type Target: callable
        @return: True if callable was successfully unregistered, False if it wasn't registered first.
        @rtype: bool
        '''

        for e in self._EventHandlers[Event]:
            if e() == Target:
                self._EventHandlers[Event].remove(e)
                return True
        return False

    def _SetDefaultEventHandler(self, Event, Target):
        if Target:
            if not callable(Target):
                raise TypeError('%s is not callable' % repr(Target))
            self._DefaultEventHandlers[Event] = WeakCallableRef(Target)
        else:
            try:
                del self._DefaultEventHandlers[Event]
            except KeyError:
                pass

    def _GetDefaultEventHandler(self, Event):
        try:
            return self._DefaultEventHandlers[Event]()
        except KeyError:
            pass

    def _SetEventHandlerObj(self, Obj):
        '''Registers an object (Obj) as event handler, object should contain methods with names
        corresponding to event names, only one obj is allowed at a time.
        '''
        self._EventHandlerObj = Obj

    @classmethod
    def _AddEvents(cls, klass):
        '''Adds events to class based on 'klass' attributes.'''
        def make_event(Event):
            return property(lambda self: self._GetDefaultEventHandler(Event),
                            lambda self, value: self._SetDefaultEventHandler(Event, value))
        for event in dir(klass):
            if not event.startswith('_'):
                setattr(cls, 'On%s' % event, make_event(event))


class Cached(object):
    '''Base class for cached objects.

    Every object is identified by an Id specified as first parameter of the constructor.
    Trying to create two objects with same Id yields the same object. Uses weak references
    to allow the objects to be deleted normally.

    WARNING!
    __init__() is always called, don't use it to prevent initializing an already
    initialized object. Use _Init() instead, it is called only once.
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

    def __copy__(self):
        return self

