'''Utility functions and classes used internally by Skype4Py.
'''

import sys
import weakref
import threading
from new import instancemethod


__all__ = ['use_generators', 'gen', 'tounicode', 'path2unicode', 'unicode2path',
           'chop', 'args2dict', 'quote', 'split', 'cndexp', 'WeakCallableRef',
           'EventHandlingBase', 'Cached']


# Disabled by default for backward compatibility.
generators_enabled = False


def use_generators(yes=True):
    '''Enables or disables the use of generator objects throughout Skype4Py.
    If generator objects are enabled, whenever Skype4Py is expected to return
    a collection (usually a tuple), a generator object will be returned instead.
    
    Generators are disabled by default for backward compatibility.
    
    New in 1.0.31.1.

    @param yes: True/False enables/disables the generator objects.
    @type yes: bool
    '''
    global generators_enabled
    generators_enabled = yes


def gen(genobj, fallback=tuple):
    '''Takes a generator object and returns it unchanged if generators were
    enabled using L{use_generators}. Otherwise falls back to the type passed
    using fallback argument, which is a tuple by default.

    @param genobj: Generator object to be processed.
    @type genobj: generator object
    @param fallback: Fallback collection type, normally a list or tuple.
    @return: Unchanged generator or converted to the fallback type.
    '''
    global generators_enabled
    if generators_enabled:
        return genobj
    return fallback(genobj)


def tounicode(s):
    '''Converts a string to a unicode string. Accepts two types or arguments. An UTF-8 encoded
    byte string or a unicode string (in the latter case, no conversion is performed).
    
    @param s: String to convert to unicode.
    @type s: str or unicode
    @return: A unicode string being the result of the conversion.
    @rtype: unicode
    '''
    if isinstance(s, unicode):
        return s
    return s.decode('utf-8')
    
    
def path2unicode(path):
    '''Decodes a file/directory path from the current file system encoding to unicode.
    
    @param path: Encoded path.
    @type path: str
    @return: Decoded path.
    @rtype: unicode
    '''
    return path.decode(sys.getfilesystemencoding())
    

def unicode2path(path):
    '''Encodes a file/directory path from unicode to the current file system encoding.
    
    @param path: Decoded path.
    @type path: unicode
    @return: Encoded path.
    @rtype: str
    '''
    return path.encode(sys.getfilesystemencoding())


def chop(s, n=1, d=None):
    '''Chops initial words from a string and returns a list of them and the rest of the string.
    The returned list is guaranteed to be n+1 long. If too little words are found in the string,
    a ValueError exception is raised.

    @param s: String to chop from.
    @type s: str or unicode
    @param n: Number of words to chop.
    @type n: int
    @param d: Optional delimiter. Any white-char by default.
    @type d: str or unicode
    @return: A list of n first words from the string followed by the rest of the string
    (C{[w1, w2, ..., wn, rest_of_string]}).
    @rtype: list of: str or unicode
    '''

    spl = s.split(d, n)
    if len(spl) == n:
        spl.append(s[:0])
    if len(spl) != n + 1:
        raise ValueError('chop: Could not chop %d words from \'%s\'' % (n, s))
    return spl


def args2dict(s):
    '''Converts a string or comma-separated 'ARG="a value"' or 'ARG=value2' strings
    into a dictionary.

    @param s: Input string.
    @type s: str or unicode
    @return: C{{'ARG': 'value'}} dictionary.
    @rtype: dict
    '''

    d = {}
    while s:
        t, s = chop(s, 1, '=')
        if s.startswith('"'):
            # XXX: This function is used to parse strings from Skype. The question is,
            # how does it escape the double-quotes. The code below implements the
            # VisualBasic technique ("" -> ").
            i = 0
            while True:
                i = s.find('"', i+1)
                try:
                    if s[i+1] != '"':
                        break
                    else:
                        i += 1
                except IndexError:
                    break
            if i > 0:
                d[t] = s[1:i].replace('""', '"')
                s = s[i+1:]
            else:
                d[t] = s
                break
        else:
            i = s.find(', ')
            if i >= 0:
                d[t] = s[:i]
                s = s[i+2:]
            else:
                d[t] = s
                break
    return d


def quote(s, always=False):
    '''Adds double-quotes to string if it contains spaces.

    @param s: String to add double-quotes to.
    @type s: str or unicode
    @param always: If True, adds quotes even if the input string contains no spaces.
    @type always: bool
    @return: If the given string contains spaces or <always> is True, returns the string enclosed
    in double-quotes. Otherwise returns the string unchanged.
    @rtype: str or unicode
    '''

    if always or ' ' in s:
        return '"%s"' % s.replace('"', '""') # VisualBasic double-quote escaping.
    return s


def split(s, d=None):
    '''Splits a string.

    @param s: String to split.
    @type s: str or unicode
    @param d: Optional delimiter. Any white-char by default.
    @type d: str or unicode
    @return: A list of words or C{[]} if the string was empty.
    @rtype: list of str or unicode
    @note: This function works like C{s.split(d)} except that it always returns an
    empty list instead of C{['']} for empty strings.
    '''

    if s:
        return s.split(d)
    return []


def cndexp(condition, truevalue, falsevalue):
    '''Simulates a conditional expression known from C or Python 2.5.

    @param condition: Tells what should be returned.
    @type condition: any
    @param truevalue: Value returned if condition evaluates to True.
    @type truevalue: any
    @param falsevalue: Value returned if condition evaluates to False.
    @type falsevalue: any
    @return: Either truevalue or falsevalue depending on condition.
    @rtype: same as type of truevalue or falsevalue
    '''

    if condition:
        return truevalue
    return falsevalue


class WeakMethod(object):
    '''Helper class for WeakCallableRef function (see below).
    Don't use directly.
    '''

    def __init__(self, method, callback=None):
        '''__init__.

        @param method: Method to be referenced.
        @type method: method
        @param callback: Callback to be called when the method is garbage collected.
        @type callback: callable
        '''
        self.im_func = method.im_func
        try:
            self.weak_im_self = weakref.ref(method.im_self, self._dies)
        except TypeError:
            self.weak_im_self = None
        self.im_class = method.im_class
        self.callback = callback

    def __call__(self):
        if self.weak_im_self:
            im_self = self.weak_im_self()
            if im_self is None:
                return None
        else:
            im_self = None
        return instancemethod(self.im_func, im_self, self.im_class)

    def __repr__(self):
        obj = self()
        objrepr = repr(obj)
        if obj is None:
            objrepr = 'dead'
        return '<weakref at 0x%x; %s>' % (id(self), objrepr)

    def _dies(self, ref):
        # weakref to im_self died
        self.im_func = self.im_class = None
        if self.callback is not None:
            self.callback(self)


def WeakCallableRef(c, callback=None):
    '''Creates and returns a new weak reference to a callable object.

    In contrast to weakref.ref() works on all kinds of callables.
    Usage is same as weakref.ref().

    @param c: A callable that the weak reference should point to.
    @type c: callable
    @param callback: Callback called when the callable is garbage collected (freed).
    @type callback: callable
    @return: A weak callable reference.
    @rtype: weakref
    '''

    try:
        return WeakMethod(c, callback)
    except AttributeError:
        return weakref.ref(c, callback)


class EventHandlingThread(threading.Thread):
    def __init__(self, name=None):
        '''__init__.

        @param name: name
        @type name: unicode
        '''
        threading.Thread.__init__(self, name='%s event handler' % name)
        self.setDaemon(False)
        self.lock = threading.Lock()
        self.queue = []

    def enqueue(self, target, args, kwargs):
        '''enqueue.

        @param target: Callable to be called.
        @type target: callable
        @param args: Positional arguments for the callable.
        @type args: tuple
        @param kwargs: Keyword arguments for the callable.
        @type kwargs: dict
        '''
        self.queue.append((target, args, kwargs))

    def run(self):
        '''Executes all queued targets.
        '''
        while True:
            try:
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
    '''This class is used as a base by all classes implementing event handlers.

    Look at known subclasses (above in epydoc) to see which classes will allow you to
    attach your own callables (event handlers) to certain events occuring in them.

    Read the respective classes documentations to learn what events are provided by them. The
    events are always defined in a class whose name consist of the name of the class it provides
    events for followed by C{Events}). For example class L{Skype} provides events defined in
    L{SkypeEvents}. The events class is always defined in the same module as the main class.

    The events class tells you what events you can assign your event handlers to, when do they
    occur and what arguments lists should your event handlers accept.

    There are three ways of attaching an event handler to an event.

      1. C{Events} object.

         Use this method if you need to attach many event handlers to many events.

         Write your event handlers as methods of a class. The superclass of your class
         is not important for Skype4Py, it will just look for methods with appropriate names.
         The names of the methods and their arguments lists can be found in respective events
         classes (see above).

         Pass an instance of this class as the C{Events} argument to the constructor of
         a class whose events you are interested in. For example::

             import Skype4Py

             class MySkypeEvents:
                 def UserStatus(self, Status):
                     print 'The status of the user changed'

             skype = Skype4Py.Skype(Events=MySkypeEvents())

         The C{UserStatus} method will be called when the status of the user currently logged
         into Skype is changed.

      2. C{On...} properties.

         This method lets you use any callables as event handlers. Simply assign them to C{On...}
         properties (where "C{...}" is the name of the event) of the object whose events you are
         interested in. For example::

             import Skype4Py

             def user_status(Status):
                 print 'The status of the user changed'

             skype = Skype4Py.Skype()
             skype.OnUserStatus = user_status

         The C{user_status} function will be called when the status of the user currently logged
         into Skype is changed.

         The names of the events and their arguments lists should be taken from respective events
         classes (see above). Note that there is no C{self} argument (which can be seen in the events
         classes) simply because our event handler is a function, not a method.

      3. C{RegisterEventHandler} / C{UnregisterEventHandler} methods.

         This method, like the second one, also lets you use any callables as event handlers. However,
         it additionally lets you assign many event handlers to a single event.

         In this case, you use L{RegisterEventHandler} and L{UnregisterEventHandler} methods
         of the object whose events you are interested in. For example::

             import Skype4Py

             def user_status(Status):
                 print 'The status of the user changed'

             skype = Skype4Py.Skype()
             skype.RegisterEventHandler('UserStatus', user_status)

         The C{user_status} function will be called when the status of the user currently logged
         into Skype is changed.

         The names of the events and their arguments lists should be taken from respective events
         classes (see above). Note that there is no C{self} argument (which can be seen in the events
         classes) simply because our event handler is a function, not a method.
         
         All handlers attached to a single event will be called serially in the order they were
         attached.

    B{Important notes!}

    The event handlers are always called on a separate thread. At any given time, there is at most
    one handling thread per event type. This means that when a lot of events of the same type are
    generated at once, their handlers will be called in serial. Handling of events of different types
    may happen simultaneously.

    In case of second and third method, only weak references to the event handlers are stored. This
    means that you must make sure that Skype4Py is not the only one having a reference to the callable
    or else it will be garbage collected and silently removed from Skype4Py's handlers list. On the
    other hand, it frees you from worrying about cyclic references.
    '''

    _EventNames = []

    def __init__(self):
        '''Initializes the object.
        '''
        self._EventHandlerObj = None
        self._DefaultEventHandlers = {}
        self._EventHandlers = {}
        self._EventThreads = {}

        for event in self._EventNames:
            self._EventHandlers[event] = []

    def _CallEventHandler(self, Event, *Args, **KwArgs):
        '''Calls all event handlers defined for given Event (str), additional parameters
        will be passed unchanged to event handlers, all event handlers are fired on
        separate threads.
        '''
        # get list of relevant handlers
        handlers = dict([(x, x()) for x in self._EventHandlers[Event]])
        if None in handlers.values():
            # cleanup
            self._EventHandlers[Event] = list([x[0] for x in handlers.items() if x[1] is not None])
        handlers = filter(None, handlers.values())
        # try the On... handlers
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
                t = self._EventThreads[Event] = EventHandlingThread(Event)
        else:
            t = self._EventThreads[Event] = EventHandlingThread(Event)
        # enqueue handlers in thread
        for h in handlers:
            t.enqueue(h, Args, KwArgs)
        # start serial event processing
        try:
            t.lock.release()
        except:
            t.start()

    def RegisterEventHandler(self, Event, Target):
        '''Registers any callable as an event handler.

        @param Event: Name of the event. For event names, see the respective C{...Events} class.
        @type Event: str
        @param Target: Callable to register as the event handler.
        @type Target: callable
        @return: True is callable was successfully registered, False if it was already registered.
        @rtype: bool
        @see: L{EventHandlingBase}
        '''

        if not callable(Target):
            raise TypeError('%s is not callable' % repr(Target))
        if Event not in self._EventHandlers:
            raise ValueError('%s is not a valid %s event name' % (Event, self.__class__.__name__))
        # get list of relevant handlers
        handlers = dict([(x, x()) for x in self._EventHandlers[Event]])
        if None in handlers.values():
            # cleanup
            self._EventHandlers[Event] = list([x[0] for x in handlers.items() if x[1] is not None])
        if Target in handlers.values():
            return False
        self._EventHandlers[Event].append(WeakCallableRef(Target))
        return True

    def UnregisterEventHandler(self, Event, Target):
        '''Unregisters a previously registered event handler (a callable).

        @param Event: Name of the event. For event names, see the respective C{...Events} class.
        @type Event: str
        @param Target: Callable to unregister.
        @type Target: callable
        @return: True if callable was successfully unregistered, False if it wasn't registered first.
        @rtype: bool
        @see: L{EventHandlingBase}
        '''

        if not callable(Target):
            raise TypeError('%s is not callable' % repr(Target))
        if Event not in self._EventHandlers:
            raise ValueError('%s is not a valid %s event name' % (Event, self.__class__.__name__))
        # get list of relevant handlers
        handlers = dict([(x, x()) for x in self._EventHandlers[Event]])
        if None in handlers.values():
            # cleanup
            self._EventHandlers[Event] = list([x[0] for x in handlers.items() if x[1] is not None])
        for wref, trg in handlers.items():
            if trg == Target:
                self._EventHandlers[Event].remove(wref)
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

    @staticmethod
    def __AddEvents_make_event(Event):
        # TODO: rework to make compatible with cython (someday?)
        return property(lambda self: self._GetDefaultEventHandler(Event),
                        lambda self, value: self._SetDefaultEventHandler(Event, value))

    @classmethod
    def _AddEvents(cls, Class):
        '''Adds events to class based on 'Class' attributes.'''
        for event in dir(Class):
            if not event.startswith('_'):
                setattr(cls, 'On%s' % event, cls.__AddEvents_make_event(event))
                cls._EventNames.append(event)


class Cached(object):
    '''Base class for all cached objects.

    Every object is identified by an Id specified as first parameter of the constructor.
    Trying to create two objects with same Id yields the same object. Uses weak references
    to allow the objects to be deleted normally.

    @warning: C{__init__()} is always called, don't use it to prevent initializing an already
    initialized object. Use C{_Init()} instead, it is called only once.
    '''
    _Cache = weakref.WeakValueDictionary()

    def __new__(cls, Id, *Args, **KwArgs):
        h = cls, Id
        try:
            return cls._Cache[h]
        except KeyError:
            o = object.__new__(cls)
            cls._Cache[h] = o
            o._Init(Id, *Args, **KwArgs)
            return o
            
    def _Init(self, Id):
        pass

    def __copy__(self):
        return self
