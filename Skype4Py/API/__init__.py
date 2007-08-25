'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from sys import builtin_module_names
import threading
from Skype4Py.utils import *
from Skype4Py.enums import *


class ICommand(object):
    def __init__(self, Id, Command, Expected=u'', Blocking=False, Timeout=30000):
        self.Id = Id
        self.Command = unicode(Command)
        self.Expected = unicode(Expected)
        self.Blocking = Blocking
        self.Timeout = Timeout
        self.Reply = u''

    def __repr__(self):
        return 'ICommand(Id=%s, Command=%s, Expected=%s, Blocking=%s, Timeout=%s, Reply=%s)' % \
            (self.Id, repr(self.Command), repr(self.Expected), self.Blocking, self.Timeout, repr(self.Reply))


class ISkypeAPIBase(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.FriendlyName = u'Skype4Py'
        self.Protocol = 5
        self.Commands = {}
        self.Handlers = []
        self.AttachmentStatus = apiAttachUnknown

    def _NotImplemented(self):
        raise ISkypeAPIError('Functionality not implemented')

    def RegisterHandler(self, Handler):
        for h in self.Handlers:
            if h() == Handler:
                return
        self.Handlers.append(WeakCallableRef(Handler))

    def UpdateHandlers(self):
        self.Handlers = filter(lambda x: x(), self.Handlers)

    def NumOfHandlers(self):
        self.UpdateHandlers()
        return len(self.Handlers)

    def CallHandler(self, mode, arg):
        for h in self.Handlers:
            f = h()
            if f:
                f(mode, arg)

    def Close(self):
        pass

    def SetFriendlyName(self, FriendlyName):
        self.FriendlyName = FriendlyName

    def SetAttachmentStatus(self, AttachmentStatus):
        if AttachmentStatus != self.AttachmentStatus:
            self.AttachmentStatus = AttachmentStatus
            self.CallHandler('attach', AttachmentStatus)

    def Attach(self, Timeout):
        self._NotImplemented()

    def IsRunning(self):
        self._NotImplemented()

    def Start(self, Minimized=False, Nosplash=False):
        self._NotImplemented()

    def Shutdown(self):
        self._NotImplemented()

    def SendCommand(self, Command):
        self._NotImplemented()

    def ApiSecurityContextEnabled(self, Context):
        self._NotImplemented()

    def EnableApiSecurityContext(self, Context):
        self._NotImplemented()


# Select apropriate low-level Skype API module
if 'posix' in builtin_module_names:
    from posix import *
elif 'nt' in builtin_module_names:
    from nt import *
else:
    raise OSError('OS not supported')
