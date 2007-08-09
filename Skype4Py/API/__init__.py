'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from sys import builtin_module_names
import threading
import weakref


class ICommand(object):
    def __init__(self, Id, Command, Expected=u'', Blocking=False, Timeout=30000):
        self.Id = Id
        self.Command = unicode(Command)
        self.Expected = unicode(Expected)
        self.Blocking = Blocking
        self.Timeout = Timeout
        self.Reply = u''


class ISkypeAPIBase(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.FriendlyName = u'Skype4Py'
        self.Protocol = 5
        self.Commands = {}
        self.Handlers = []

    def RegisterHandler(self, Handler):
        r = weakref.ref(Handler.im_self), Handler.im_func
        if r not in self.Handlers:
            self.Handlers.append(r)

    def UpdateHandlers(self):
        alive = []
        for h in self.Handlers:
            if h[0]():
                alive.append(h)
        self.Handlers = alive

    def NumOfHandlers(self):
        self.UpdateHandlers()
        return len(self.Handlers)

    def CallHandler(self, mode, arg):
        for h in self.Handlers:
            o = h[0]()
            if o:
                h[1](o, mode, arg)

    def Close(self):
        pass

    def SetFriendlyName(self, FriendlyName):
        self.FriendlyName = FriendlyName

    def Attach(self, Timeout):
        pass

    def IsRunning(self):
        pass

    def Start(self, Minimized=False, Nosplash=False):
        pass

    def Shutdown(self):
        pass

    def SendCommand(self, Command):
        pass


# Select apropriate low-level Skype API module
if 'posix' in builtin_module_names:
    from posix import *
elif 'nt' in builtin_module_names:
    from nt import *
else:
    raise OSError('OS not supported')
