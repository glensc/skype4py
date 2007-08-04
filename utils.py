
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

    The 'events' is a list of events names. The class
    will contain 'On...' properties (where '...' is a event name) which can be set to callables. The
    class contains a _CallEventHandler() method which can be used to call the handlers. It expects the
    name of event as argument. The name can be followed by further arguements which will be passed
    unchanged to the event handler. The class constructor expects one argument - an Events class.
    This class may contain methods named after the events (without the 'On'). The _CallEventHandler()
    method will first try to call the handlers assigned to 'On...' properties and if this cannot be done
    (because the property wasn't set), it will try to call the handler in an instatinated Events class.
    '''

    class EventHandlingBase(object):
        def __init__(self):
            self._Events = {}
            self._EventHandlers = {}

        def _CallEventHandler(self, name, *args, **kwargs):
            d = self._EventHandlers.get(name, {})
            for h in d:
                threading.Thread(name=name, target=d[h], args=args, kwargs=kwargs).start()
            d = self._Events
            for h in d:
                if hasattr(d[h], name):
                    threading.Thread(name=name, target=getattr(d[h], name), args=args, kwargs=kwargs).start()

        def _GetEventHandler(self, name):
            try:
                return self._EventHandlers.get(name, {})['default']
            except KeyError:
                return None

        def _SetEventHandler(self, name, target):
            if callable(target):
                self._RegisterEventHandler(name, 'default', target)
            elif target == None:
                self._UnregisterEventHandler(name, 'default')
            else:
                raise ValueError('%s is not callable' % repr(target))

        def _RegisterEventHandler(self, name, info, target):
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

        def _RegisterEventsClass(self, cls):
            self._Events[cls] = cls()

        def _UnregisterEventsClass(self, cls):
            try:
                del self._Events[cls]
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
        if not event.startswith('_'):
            setattr(EventHandlingBase, 'On' + event, make_event(event))
    return EventHandlingBase


class EnumItem(object):
    ''' The instances of this class are enum values. They should be instatinated by the Enum class,
    not directly.
    '''

    def __init__(self, c, n, s, i):
        self.c = str(c)
        self.n = str(n)
        self.s = str(s)
        self.i = int(i)

    def __repr__(self):
        return '%s.%s' % (self.c, self.n)

    def __str__(self):
        return self.s

    def __int__(self):
        return self.i

    def __eq__(self, other):
        if type(other) in [type(str()), type(unicode())]:
            return self.s.upper() == other.upper()
        elif type(other) in [type(int()), type(long())]:
            return self.i == other
        elif type(other) == EnumItem:
            return (self.c, self.n) == (other.c, other.n)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


def GetEnumMetaClass():
    ''' Creates a metaclass for Enum class.
    '''

    class EnumMetaClass(object):
        def __init__(self, name, bases, classdict):
            self.__name__ = name
            _all_ = []
            i = -1
            for x in classdict.get('_enum_', []):
                if len(x) > 2:
                    i = x[2]
                item = EnumItem(name, x[0], x[1], i)
                _all_.append(item)
                setattr(self, x[0], item)
                i += 1
            self._all_ = _all_

        def __call__(self, init=None):
            if init == None:
                return self._all_[0]
            elif type(init) == EnumItem:
                return init
            try:
                return self._all_[self._all_.index(init)]
            except ValueError:
                raise ValueError('\'%s\' does not belong to %s enum' % (str(init), self.__name__))

        def __contains__(self, item):
            return item in self._all_

        def __len__(self):
            return len(self._all_)

        def __getitem__(self, n):
            return self._all_[n]

    return EnumMetaClass


class Enum(object):
    ''' This is the base class for enum types. Enum types should be defined as follows:

    class Colors(Enum):
        _enum_ = [('Red', 'RED'),
                  ('Green', 'GREEN'),
                  ('Blue', 'BLUE')]

    This definition will cause Colors.Red, Colors.Green and Colors.Blue values to be available.
    The values will be of type EnumItem. Passing them to repr() will return their name with
    enum name, for example 'Colors.Red'. Passing to str() will return the string given as second
    item of _enum_ tuples (for example 'RED'). It can also be passed to int() which in the given
    example will always return -1 but it can be changed by specifying the integer as third item
    of _enum_ tuples.

    Calling Colors(x) will create an EnumItem. The parameter can be either a string or an
    integer passed as second and third item of _enum_ tuples.
    '''
    __metaclass__ = GetEnumMetaClass()


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
