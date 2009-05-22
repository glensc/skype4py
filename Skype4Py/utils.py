'''Utility functions and classes used internally by Skype4Py.
'''
__docformat__ = 'restructuredtext en'


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

    :Parameters:
      yes : bool
        True/False enables/disables the generator objects.
    '''
    global generators_enabled
    generators_enabled = yes


def gen(genobj, fallback=tuple):
    '''Takes a generator object and returns it unchanged if generators were
    enabled using `use_generators`. Otherwise falls back to the type passed
    using fallback argument, which is a tuple by default.

    :Parameters:
      genobj : generator object
        Generator object to be processed.
      fallback
        Fallback collection type, normally a list or tuple.

    :return: Unchanged generator or converted to the fallback type.
    '''
    global generators_enabled
    if generators_enabled:
        return genobj
    return fallback(genobj)


def tounicode(s):
    '''Converts a string to a unicode string. Accepts two types or arguments. An UTF-8 encoded
    byte string or a unicode string (in the latter case, no conversion is performed).

    :Parameters:
      s : str or unicode
        String to convert to unicode.

    :return: A unicode string being the result of the conversion.
    :rtype: unicode
    '''
    if isinstance(s, unicode):
        return s
    return s.decode('utf-8')
    
    
def path2unicode(path):
    '''Decodes a file/directory path from the current file system encoding to unicode.

    :Parameters:
      path : str
        Encoded path.

    :return: Decoded path.
    :rtype: unicode
    '''
    return path.decode(sys.getfilesystemencoding())
    

def unicode2path(path):
    '''Encodes a file/directory path from unicode to the current file system encoding.

    :Parameters:
      path : unicode
        Decoded path.

    :return: Encoded path.
    :rtype: str
    '''
    return path.encode(sys.getfilesystemencoding())


def chop(s, n=1, d=None):
    '''Chops initial words from a string and returns a list of them and the rest of the string.
    The returned list is guaranteed to be n+1 long. If too little words are found in the string,
    a ValueError exception is raised.

    :Parameters:
      s : str or unicode
        String to chop from.
      n : int
        Number of words to chop.
      d : str or unicode
        Optional delimiter. Any white-char by default.

    :return: A list of n first words from the string followed by the rest of the string (``[w1, w2,
             ..., wn, rest_of_string]``).
    :rtype: list of: str or unicode
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

    :Parameters:
      s : str or unicode
        Input string.

    :return: ``{'ARG': 'value'}`` dictionary.
    :rtype: dict
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

    :Parameters:
      s : str or unicode
        String to add double-quotes to.
      always : bool
        If True, adds quotes even if the input string contains no spaces.

    :return: If the given string contains spaces or <always> is True, returns the string enclosed in
             double-quotes. Otherwise returns the string unchanged.
    :rtype: str or unicode
    '''

    if always or ' ' in s:
        return '"%s"' % s.replace('"', '""') # VisualBasic double-quote escaping.
    return s


def split(s, d=None):
    '''Splits a string.

    :Parameters:
      s : str or unicode
        String to split.
      d : str or unicode
        Optional delimiter. Any white-char by default.

    :return: A list of words or ``[]`` if the string was empty.
    :rtype: list of str or unicode

    :note: This function works like ``s.split(d)`` except that it always returns an empty list
           instead of ``['']`` for empty strings.
    '''

    if s:
        return s.split(d)
    return []


def cndexp(condition, truevalue, falsevalue):
    '''Simulates a conditional expression known from C or Python 2.5.

    :Parameters:
      condition : any
        Tells what should be returned.
      truevalue : any
        Value returned if condition evaluates to True.
      falsevalue : any
        Value returned if condition evaluates to False.

    :return: Either truevalue or falsevalue depending on condition.
    :rtype: same as type of truevalue or falsevalue
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

        :Parameters:
          method : method
            Method to be referenced.
          callback : callable
            Callback to be called when the method is garbage collected.
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

    :Parameters:
      c : callable
        A callable that the weak reference should point to.
      callback : callable
        Callback called when the callable is garbage collected (freed).

    :return: A weak callable reference.
    :rtype: weakref
    '''

    try:
        return WeakMethod(c, callback)
    except AttributeError:
        return weakref.ref(c, callback)


class EventHandlingThread(threading.Thread):
    def __init__(self, name=None):
        '''__init__.

        :Parameters:
          name : unicode
            name
        '''
        threading.Thread.__init__(self, name='%s event handler' % name)
        self.setDaemon(False)
        self.lock = threading.Lock()
        self.queue = []

    def enqueue(self, target, args, kwargs):
        '''enqueue.

        :Parameters:
          target : callable
            Callable to be called.
          args : tuple
            Positional arguments for the callable.
          kwargs : dict
            Keyword arguments for the callable.
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
    attach your own callables (event handlers) to certain events occurring in them.

    Read the respective classes documentations to learn what events are provided by them. The
    events are always defined in a class whose name consist of the name of the class it provides
    events for followed by ``Events``). For example class `Skype` provides events defined in
    `SkypeEvents`. The events class is always defined in the same module as the main class.

    The events class tells you what events you can assign your event handlers to, when do they
    occur and what arguments lists should your event handlers accept.

    There are three ways of attaching an event handler to an event.

    1. ``Events`` object.

       Use this method if you need to attach many event handlers to many events.

       Write your event handlers as methods of a class. The superclass of your class
       is not important for Skype4Py, it will just look for methods with appropriate names.
       The names of the methods and their arguments lists can be found in respective events
       classes (see above).

       Pass an instance of this class as the ``Events`` argument to the constructor of
       a class whose events you are interested in. For example:

       .. python::

           import Skype4Py

           class MySkypeEvents:
               def UserStatus(self, Status):
                   print 'The status of the user changed'

           skype = Skype4Py.Skype(Events=MySkypeEvents())

       The ``UserStatus`` method will be called when the status of the user currently logged
       into Skype is changed.

    2. ``On...`` properties.

       This method lets you use any callables as event handlers. Simply assign them to ``On...``
       properties (where "``...``" is the name of the event) of the object whose events you are
       interested in. For example:
       
       .. python::

           import Skype4Py

           def user_status(Status):
               print 'The status of the user changed'

           skype = Skype4Py.Skype()
           skype.OnUserStatus = user_status

       The ``user_status`` function will be called when the status of the user currently logged
       into Skype is changed.

       The names of the events and their arguments lists should be taken from respective events
       classes (see above). Note that there is no ``self`` argument (which can be seen in the events
       classes) simply because our event handler is a function, not a method.

    3. ``RegisterEventHandler`` / ``UnregisterEventHandler`` methods.

       This method, like the second one, also lets you use any callables as event handlers. However,
       it additionally lets you assign many event handlers to a single event.

       In this case, you use `RegisterEventHandler` and `UnregisterEventHandler` methods
       of the object whose events you are interested in. For example:
       
       .. python::

           import Skype4Py

           def user_status(Status):
               print 'The status of the user changed'

           skype = Skype4Py.Skype()
           skype.RegisterEventHandler('UserStatus', user_status)

       The ``user_status`` function will be called when the status of the user currently logged
       into Skype is changed.

       The names of the events and their arguments lists should be taken from respective events
       classes (see above). Note that there is no ``self`` argument (which can be seen in the events
       classes) simply because our event handler is a function, not a method.
       
       All handlers attached to a single event will be called serially in the order they were
       attached.

    **Multithreading warning.**

    The event handlers are always called on a separate thread. At any given time, there is at most
    one handling thread per event type. This means that when a lot of events of the same type are
    generated at once, their handlers will be called in serial on one thread. Handling of events
    of different types may happen simultaneously on many threads.
    
    **Object owning note.**

    In the first method, a reference to the events object is stored. However, in the second and
    third method, only weak references to the event handlers are maintained. This means that you
    must make sure that Skype4Py is not the only one having a reference to the callable or else
    it will be garbage collected and silently removed from Skype4Py's handlers list. On the other
    hand, it frees you from worrying about cyclic references.
    
    Skype4Py uses its own mechanism for weak references to callables (`WeakCallableRef`) which
    properly handles weak references to all types of Python callables.
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
        '''Calls all event handlers defined for given Event, additional parameters
        will be passed unchanged to event handlers, all event handlers are fired on
        separate threads.
        
        :Parameters:
          Event : str
            Name of the event.
          Args
            Positional arguments for the event handlers.
          KwArgs
            Keyword arguments for the event handlers.
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

        :Parameters:
          Event : str
            Name of the event. For event names, see the respective ``...Events`` class.
          Target : callable
            Callable to register as the event handler.

        :return: True is callable was successfully registered, False if it was already registered.
        :rtype: bool

        :see: `EventHandlingBase`
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

        :Parameters:
          Event : str
            Name of the event. For event names, see the respective ``...Events`` class.
          Target : callable
            Callable to unregister.

        :return: True if callable was successfully unregistered, False if it wasn't registered
                 first.
        :rtype: bool

        :see: `EventHandlingBase`
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
        '''Registers an object as events handler, object should contain methods with names
        corresponding to event names, only one object may be registered at a time. A reference
        to the object will be kept until it is unregistered.
        
        :Parameters:
          Obj
            Object to register. If None, unregisters the currently registered object.
        '''
        self._EventHandlerObj = Obj

    @staticmethod
    def __AddEvents_make_event(Event):
        # TODO: rework to make compatible with cython (someday?)
        return property(lambda self: self._GetDefaultEventHandler(Event),
                        lambda self, value: self._SetDefaultEventHandler(Event, value))

    @classmethod
    def _AddEvents(cls, Class):
        '''Adds events to class based on the attributes of the given class.
        
        :Parameters:
          Class : class
            An `...Events` class whose methods define events that may occur in the
            instances of the current class.
        '''
        for event in dir(Class):
            if not event.startswith('_'):
                setattr(cls, 'On%s' % event, cls.__AddEvents_make_event(event))
                cls._EventNames.append(event)


class Cached(object):
    '''Base class for all cached objects.
    
    Every object has an owning object a handle. Owning object is where the cache is
    maintained, handle identifies an object of given type.
    
    Thanks to the caching, trying to create two objects with the same owner and handle
    yields exactly the same object. The cache itself is based on weak references so
    not referenced objects are automatically removed from the cache.

    Because the ``__init__`` method will be called no matter if the object already
    existed or not, it is recommended to use the `_Init` method instead.
    '''
    _HandleCast = None

    def __new__(cls, Owner, Handle, *Args, **KwArgs):
        if cls._HandleCast is not None:
            Handle = cls._HandleCast(Handle)
        key = cls, Handle
        try:
            return Owner._ObjectCache[key]
        except KeyError:
            obj = object.__new__(cls)
            Owner._ObjectCache[key] = obj
            obj._Init(Owner, Handle, *Args, **KwArgs)
            return obj
            
    def _Init(self, Owner, Handle):
        '''Initializes the cached object. Receives all the arguments passed to the
        constructor The default implementation stores the ``Owner`` in
        ``self._Owner`` and ``Handle`` in ``self._Handle``.
        
        This method should be used instead of ``__init__`` to prevent double
        initialization.
        '''
        self._Owner = Owner
        self._Handle = Handle

    def __copy__(self):
        return self
        
    def _MakeOwner(self):
        '''Prepares the object for use as an owner for other cached objects.
        '''
        self._CreateOwner(self)

    @classmethod
    def _CreateOwner(cls, Owner):
        '''Prepares any object for use as an owner for cached objects.
        
        :Parameters:
          Owner
            Object that should be turned into a cached objects owner.
        '''
        Owner._ObjectCache = weakref.WeakValueDictionary()
