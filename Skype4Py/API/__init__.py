'''
Low-level Skype API definitions.

This module imports one of the:
  - L{Skype4Py.API.darwin}
  - L{Skype4Py.API.posix}
  - L{Skype4Py.API.windows}
submodules based on the current platform.
'''

import sys
import threading
from Skype4Py.utils import *
from Skype4Py.enums import *
from Skype4Py.errors import SkypeAPIError


class Command(object):
    '''Represents an API command. Use L{Skype.Command<skype.Skype.Command>} to instatinate.

    To send a command to Skype, use L{Skype.SendCommand<skype.Skype.SendCommand>}.
    '''

    def __init__(self, Id, Command, Expected=u'', Blocking=False, Timeout=30000):
        '''Use L{Skype.Command<skype.Skype.Command>} to instatinate the object instead.
        '''

        self.Blocking = Blocking
        '''If set to True, L{Skype.SendCommand<skype.Skype.SendCommand>} will block until the reply is received.
        @type: bool'''

        self.Command = tounicode(Command)
        '''Command string.
        @type: unicode'''

        self.Expected = tounicode(Expected)
        '''Expected reply.
        @type: unicode'''

        self.Id = Id
        '''Command Id.
        @type: int'''

        self.Reply = u''
        '''Reply after the command has been sent and Skype has replied.
        @type: unicode'''

        self.Timeout = Timeout
        '''Timeout in milliseconds if Blocking=True.
        @type: int'''

    def __repr__(self):
        return '<%s with Id=%s, Command=%s, Blocking=%s, Reply=%s>' % \
            (object.__repr__(self)[1:-1], self.Id, repr(self.Command), self.Blocking, repr(self.Reply))


class SkypeAPIBase(threading.Thread):
    def __init__(self, opts):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.DebugLevel = opts.pop('ApiDebugLevel', 0)
        self.FriendlyName = u'Skype4Py'
        self.Protocol = 5
        self.Commands = {}
        self.CommandsLock = threading.Lock()
        self.Handlers = []
        self.AttachmentStatus = apiAttachUnknown

    def _NotImplemented(self):
        raise SkypeAPIError('Functionality not implemented')

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

    def CommandsStackPush(self, command):
        self.CommandsLock.acquire()
        if command.Id < 0:
            command.Id = 0
            while command.Id in self.Commands:
                command.Id += 1
        if command.Id in self.Commands:
            self.CommandsLock.release()
            raise SkypeAPIError('Command Id conflict')
        self.Commands[command.Id] = command
        self.CommandsLock.release()

    def CommandsStackPop(self, Id):
        self.CommandsLock.acquire()
        try:
            command = self.Commands[Id]
            del self.Commands[Id]
        except KeyError:
            command = None
        self.CommandsLock.release()
        return command

    def Close(self):
        pass

    def SetDebugLevel(self, Level):
        self.DebugLevel = Level

    def DebugPrint(self, *args, **kwargs):
        if self.DebugLevel >= kwargs.get('Level', 1):
            print >>sys.stderr, 'Skype4Py/API', ' '.join(('%s',) * len(args)) % args

    def SetFriendlyName(self, FriendlyName):
        self.FriendlyName = FriendlyName

    def SetAttachmentStatus(self, AttachmentStatus):
        if AttachmentStatus != self.AttachmentStatus:
            self.DebugPrint('AttachmentStatus', AttachmentStatus)
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


# Select appropriate low-level Skype API module
if sys.platform[:3] == 'win':
    from windows import SkypeAPI
elif sys.platform == 'darwin':
    from darwin import SkypeAPI
else:
    from posix import SkypeAPI
