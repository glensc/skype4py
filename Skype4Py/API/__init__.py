'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

import sys
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
        self.CommandsLock = threading.Lock()
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

    def CommandsStackPush(self, Command):
        self.CommandsLock.acquire()
        if Command.Id < 0:
            Command.Id = 0
            while Command.Id in self.Commands:
                Command.Id += 1
        if Command.Id in self.Commands:
            self.CommandsLock.release()
            raise ISkypeAPIError('Command Id conflict')
        self.Commands[Command.Id] = Command
        self.CommandsLock.release()

    def CommandsStackPop(self, Id):
        self.CommandsLock.acquire()
        try:
            Command = self.Commands[Id]
            del self.Commands[Id]
        except KeyError:
            Command = None
        self.CommandsLock.release()
        return Command

    def Close(self):
        pass

    def SetFriendlyName(self, FriendlyName):
        self.FriendlyName = FriendlyName

    def SetAttachmentStatus(self, AttachmentStatus):
        if AttachmentStatus != self.AttachmentStatus:
            self.AttachmentStatus = AttachmentStatus
            self.CallHandler('attach', AttachmentStatus)

    def Attach(self, Timeout=30000, Wait=True):
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
if sys.platform[:3] == 'win':
    from windows import ISkypeAPI
elif sys.platform == 'darwin':
    from darwin import ISkypeAPI
else:
    from posix import ISkypeAPI
