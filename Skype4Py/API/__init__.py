'''
Low-level Skype API definitions.

This module imports one of the:
  - L{Skype4Py.API.darwin}
  - L{Skype4Py.API.posix}
  - L{Skype4Py.API.windows}
submodules based on the platform.
'''

import sys
import threading
from Skype4Py.utils import *
from Skype4Py.enums import *


class ICommand(object):
    '''Represents an API command. Use L{ISkype.Command} to instatinate.

    To send a command to Skype, use L{ISkype.SendCommand}.
    '''

    def __init__(self, Id, Command, Expected=u'', Blocking=False, Timeout=30000):
        '''Use L{ISkype.Command} to instatinate the object instead.
        '''

        self.Id = Id
        '''Command Id.
        @type: int'''

        self.Command = unicode(Command)
        '''Command string.
        @type: unicode'''

        self.Expected = unicode(Expected)
        '''Expected reply.
        @type: unicode'''

        self.Blocking = Blocking
        '''If set to True, L{ISkype.SendCommand} will block until the reply is received.
        @type: bool'''

        self.Timeout = Timeout
        '''Timeout in milliseconds if Blocking=True.
        @type: int'''

        self.Reply = u''
        '''Reply after the command has been sent and Skype has replied.
        @type: unicode'''

    def __repr__(self):
        '''Returns a string representing the command with all its parameters.

        @return: Representation string.
        @rtype: str
        '''
        return 'ICommand(Id=%s, Command=%s, Expected=%s, Blocking=%s, Timeout=%s, Reply=%s)' % \
            (self.Id, repr(self.Command), repr(self.Expected), self.Blocking, self.Timeout, repr(self.Reply))


class _ISkypeAPIBase(threading.Thread):
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
    from windows import _ISkypeAPI
elif sys.platform == 'darwin':
    from darwin import _ISkypeAPI
else:
    from posix import _ISkypeAPI
