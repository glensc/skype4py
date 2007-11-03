'''
Utility functions and classes used internally by Skype4Py.
'''

import sys
import weakref
import threading
from new import instancemethod


def chop(s, n=1):
    '''Chops initial words from a string and returns a list of them and the rest of the string.

    @param s: String to chop from.
    @type s: str or unicode
    @param n: Number of words to chop.
    @type n: int
    @return: A list of n first words from the string followed by the rest of the string
    (C{[w1, w2, ..., wn, rest_of_string]}).
    @rtype: list of str or unicode
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
    '''Adds double-quotes to string if needed.

    @param s: String to add double-quotes to.
    @type s: str or unicode
    @return: If the given string contains spaces, returns the string enclosed in double-quotes
    (if it contained quotes too, they are preceded with a backslash). If the string doesn't
    contain spaces, returns the string unchanged.
    @rtype: str or unicode
    '''

    if ' ' in s:
        return '"%s"' % s.replace('"', '\\"')
    return s


def esplit(s, d=None):
    '''Splits a string into words.

    @param s: String to split.
    @type s: str or unicode
    @param d: Optional delimeter. By default any white char.
    @type d: str or unicode
    @return: A list of words or C{[]} if the string was empty.
    @rtype: list of str or unicode
    @note: This function works like C{s.split(d)} except that it returns an
    empty list instead of C{['']} for empty strings.
    '''

    if s:
        return s.split(d)
    return []


def cndexp(condition, truevalue, falsevalue):
    '''Simulates a conditional expression known from C or Python 2.5+.

    @param condition: Boolean value telling what should be returned.
    @type condition: bool, see note
    @param truevalue: Value returned if condition was True.
    @param falsevalue: Value returned if condition was False.
    @return: Either truevalue or falsevalue depending on condition.
    @note: The type of condition parameter can be anything as long as
    C{bool(condition)} returns a bool value.
    '''

    if condition:
        return truevalue
    return falsevalue


def deprecated(klass, attrold, attrnew):
    '''Prints a deprecation note to sys.stderr.

    @param klass: Name of the class with a deprecated attribute.
    @type klass: str
    @param attrold: Name of the deprecated attribute.
    @type attrold: str
    @param attrnew: Name of an attribute that should be used instead.
    @type attrnew: str
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
    Usage is same as weakref.ref().
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

    _EventNames = []

    def __init__(self):
        '''Initializes the object.'''
        self._EventHandlerObj = None
        self._DefaultEventHandlers = {}
        self._EventHandlers = {}
        self._EventThreads = {}

        for event in self._EventNames:
            self._EventHandlers[event] = []

    def _CallEventHandler(self, Event, *args, **kwargs):
        '''Calls all event handlers defined for given Event (str), additional parameters
        will be passed unchanged to event handlers, all event handlers are fired on
        separate threads.
        '''

        # get list of relevant handlers
        allhandlers = [x() for x in self._EventHandlers[Event]]
        handlers = filter(bool, allhandlers)
        if len(allhandlers) != len(handlers):
            # cleanup
            self._EventHandlers[Event] = list(x for x in self._EventHandlers[Event] if x())
        # try the OnX handlers
        try:
            h = self._DefaultEventHandlers[Event]()
            if h:
                handlers.append(h)
        except KeyError:
            pass
        # try the object handlers
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
            raise ValueError('%s is not a valid %s event name' % (Event, self.__class__.__name__))
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

        if not callable(Target):
            raise TypeError('%s is not callable' % repr(Target))
        if Event not in self._EventHandlers:
            raise ValueError('%s is not a valid %s event name' % (Event, self.__class__.__name__))
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
                cls._EventNames.append(event)


class Cached(object):
    '''Base class for all cached objects.

    Every object is identified by an Id specified as first parameter of the constructor.
    Trying to create two objects with same Id yields the same object. Uses weak references
    to allow the objects to be deleted normally.

    @warning: C{__init__()} is always called, don't use it to prevent initializing an already
    initialized object. Use C{_Init()} instead, it is called only once.
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

