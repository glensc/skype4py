'''
Low level Skype for Linux interface implemented
using XWindows messaging. Uses direct Xlib calls
through ctypes module.

This module handles the options that you can pass to L{ISkype.__init__<skype.ISkype.__init__>}
for Linux machines when the transport is set to X11.

No further options are currently supported.
'''

import threading
from ctypes import *
from ctypes.util import find_library
import time
from Skype4Py.API import ICommand, _ISkypeAPIBase
from Skype4Py.enums import *
from Skype4Py.errors import ISkypeAPIError


# some Xlib constants
_PropertyChangeMask = 0x400000
_PropertyNotify = 28
_ClientMessage = 33
_PropertyNewValue = 0
_PropertyDelete = 1


# some Xlib types
c_ulong_p = POINTER(c_ulong)
DisplayP = c_void_p
Atom = c_ulong
AtomP = c_ulong_p
XID = c_ulong
Window = XID
Bool = c_int
Status = c_int
Time = c_ulong
c_int_p = POINTER(c_int)


# should the structures be aligned to 8 bytes?
_align = (sizeof(c_long) == 8 and sizeof(c_int) == 4)


# some Xlib structures
class _XClientMessageEvent(Structure):
    if _align:
        _fields_ = [('type', c_int),
                    ('pad0', c_int),
                    ('serial', c_ulong),
                    ('send_event', Bool),
                    ('pad1', c_int),
                    ('display', DisplayP),
                    ('window', Window),
                    ('message_type', Atom),
                    ('format', c_int),
                    ('pad2', c_int),
                    ('data', c_char * 20)]
    else:
        _fields_ = [('type', c_int),
                    ('serial', c_ulong),
                    ('send_event', Bool),
                    ('display', DisplayP),
                    ('window', Window),
                    ('message_type', Atom),
                    ('format', c_int),
                    ('data', c_char * 20)]

class _XPropertyEvent(Structure):
    if _align:
        _fields_ = [('type', c_int),
                    ('pad0', c_int),
                    ('serial', c_ulong),
                    ('send_event', Bool),
                    ('pad1', c_int),
                    ('display', DisplayP),
                    ('window', Window),
                    ('atom', Atom),
                    ('time', Time),
                    ('state', c_int),
                    ('pad2', c_int)]
    else:
        _fields_ = [('type', c_int),
                    ('serial', c_ulong),
                    ('send_event', Bool),
                    ('display', DisplayP),
                    ('window', Window),
                    ('atom', Atom),
                    ('time', Time),
                    ('state', c_int)]

class _XErrorEvent(Structure):
    if _align:
        _fields_ = [('type', c_int),
                    ('pad0', c_int),
                    ('display', DisplayP),
                    ('resourceid', XID),
                    ('serial', c_ulong),
                    ('error_code', c_ubyte),
                    ('request_code', c_ubyte),
                    ('minor_code', c_ubyte)]
    else:
        _fields_ = [('type', c_int),
                    ('display', DisplayP),
                    ('resourceid', XID),
                    ('serial', c_ulong),
                    ('error_code', c_ubyte),
                    ('request_code', c_ubyte),
                    ('minor_code', c_ubyte)]

class _XEvent(Union):
    if _align:
        _fields_ = [('type', c_int),
                    ('xclient', _XClientMessageEvent),
                    ('xproperty', _XPropertyEvent),
                    ('xerror', _XErrorEvent),
                    ('pad', c_long * 24)]
    else:
        _fields_ = [('type', c_int),
                    ('xclient', _XClientMessageEvent),
                    ('xproperty', _XPropertyEvent),
                    ('xerror', _XErrorEvent),
                    ('pad', c_long * 24)]

XEventP = POINTER(_XEvent)


# load X11 library (Xlib)
libpath = find_library('X11')
if not libpath:
    raise ImportError('Could not find X11 library')
_x11 = cdll.LoadLibrary(libpath)
del libpath


# setup Xlib function prototypes
_x11.XCloseDisplay.argtypes = (DisplayP,)
_x11.XCloseDisplay.restype = None
_x11.XCreateSimpleWindow.argtypes = (DisplayP, Window, c_int, c_int, c_uint,
        c_uint, c_uint, c_ulong, c_ulong)
_x11.XCreateSimpleWindow.restype = Window
_x11.XDefaultRootWindow.argtypes = (DisplayP,)
_x11.XDefaultRootWindow.restype = Window
_x11.XDeleteProperty.argtypes = (DisplayP, Window, Atom)
_x11.XDeleteProperty.restype = None
_x11.XDestroyWindow.argtypes = (DisplayP, Window)
_x11.XDestroyWindow.restype = None
_x11.XPending.argtypes = (DisplayP,)
_x11.XPending.restype = c_int
_x11.XGetAtomName.argtypes = (DisplayP, Atom)
_x11.XGetAtomName.restype = c_char_p
_x11.XGetErrorText.argtypes = (DisplayP, c_int, c_char_p, c_int)
_x11.XGetErrorText.restype = None
_x11.XGetWindowProperty.argtypes = (DisplayP, Window, Atom, c_long, c_long, Bool,
        Atom, AtomP, c_int_p, c_ulong_p, c_ulong_p, POINTER(POINTER(Window)))
_x11.XGetWindowProperty.restype = c_int
_x11.XInitThreads.argtypes = ()
_x11.XInitThreads.restype = Status
_x11.XInternAtom.argtypes = (DisplayP, c_char_p, Bool)
_x11.XInternAtom.restype = Atom
_x11.XNextEvent.argtypes = (DisplayP, XEventP)
_x11.XNextEvent.restype = None
_x11.XOpenDisplay.argtypes = (c_char_p,)
_x11.XOpenDisplay.restype = DisplayP
_x11.XSelectInput.argtypes = (DisplayP, Window, c_long)
_x11.XSelectInput.restype = None
_x11.XSendEvent.argtypes = (DisplayP, Window, Bool, c_long, XEventP)
_x11.XSendEvent.restype = Status
_x11.XLockDisplay.argtypes = (DisplayP,)
_x11.XLockDisplay.restype = None
_x11.XUnlockDisplay.argtypes = (DisplayP,)
_x11.XUnlockDisplay.restype = None


# Enable X11 multithreading
_x11.XInitThreads()


class _ISkypeAPI(_ISkypeAPIBase):
    def __init__(self, handler, opts):
        _ISkypeAPIBase.__init__(self, opts)
        self.RegisterHandler(handler)

        # check options
        if opts:
            raise TypeError('Unexpected parameter(s): %s' % ', '.join(opts.keys()))

        # init Xlib display
        self.disp = _x11.XOpenDisplay(None)
        if not self.disp:
            raise ISkypeAPIError('Could not open XDisplay')
        self.win_root = _x11.XDefaultRootWindow(self.disp)
        self.win_self = _x11.XCreateSimpleWindow(self.disp, self.win_root,
                                    100, 100, 100, 100, 1, 0, 0)
        _x11.XSelectInput(self.disp, self.win_root, _PropertyChangeMask)
        self.win_skype = self.get_skype()
        ctrl = 'SKYPECONTROLAPI_MESSAGE'
        self.atom_msg = _x11.XInternAtom(self.disp, ctrl, False)
        self.atom_msg_begin = _x11.XInternAtom(self.disp, ctrl + '_BEGIN', False)

        self.loop_event = threading.Event()
        self.loop_timeout = 0.0001
        self.loop_break = False

    def __del__(self):
        if hasattr(self, 'x11'):
            if hasattr(self, 'disp'):
                if hasattr(self, 'win_self'):
                    _x11.XDestroyWindow(self.disp, self.win_self)
                _x11.XCloseDisplay(self.disp)

    def run(self):
        self.DebugPrint('thread started')
        # main loop
        event = _XEvent()
        data = ''
        while not self.loop_break:
            pending = _x11.XPending(self.disp)
            if not pending:
                self.loop_event.wait(self.loop_timeout)
                if self.loop_event.isSet():
                    self.loop_timeout = 0.0001
                elif self.loop_timeout < 1.0:
                    self.loop_timeout *= 2
                self.loop_event.clear()
                continue
            self.loop_timeout = 0.0001
            for i in xrange(pending):
                _x11.XLockDisplay(self.disp)
                _x11.XNextEvent(self.disp, byref(event))
                _x11.XUnlockDisplay(self.disp)
                if event.type == _ClientMessage:
                    if event.xclient.format == 8:
                        if event.xclient.message_type == self.atom_msg_begin:
                            data = str(event.xclient.data)
                        elif event.xclient.message_type == self.atom_msg:
                            if data != '':
                                data += str(event.xclient.data)
                            else:
                                print 'Warning! Middle of message received with no beginning!'
                        else:
                            continue
                        if len(event.xclient.data) != 20 and data:
                            self.notify(data.decode('utf-8'))
                            data = ''
                elif event.type == _PropertyNotify:
                    if _x11.XGetAtomName(self.disp, event.xproperty.atom) == '_SKYPE_INSTANCE':
                        if event.xproperty.state == _PropertyNewValue:
                            self.win_skype = self.get_skype()
                            # changing attachment status can cause an event handler to be fired, in
                            # turn it could try to call Attach() and doing this immediately seems to
                            # confuse Skype (command '#0 NAME xxx' returns '#0 CONNSTATUS OFFLINE' :D);
                            # to fix this, we give Skype some time to initialize itself
                            time.sleep(1.0)
                            self.SetAttachmentStatus(apiAttachAvailable)
                        elif event.xproperty.state == _PropertyDelete:
                            self.win_skype = None
                            self.SetAttachmentStatus(apiAttachNotAvailable)
        self.DebugPrint('thread finished')
   
    def get_skype(self):
        '''Returns Skype window ID or None if Skype not running.'''
        skype_inst = _x11.XInternAtom(self.disp, '_SKYPE_INSTANCE', True)
        if not skype_inst:
            return
        type_ret = Atom()
        format_ret = c_int()
        nitems_ret = c_ulong()
        bytes_after_ret = c_ulong()
        winp = pointer(Window())
        fail = _x11.XGetWindowProperty(self.disp, self.win_root, skype_inst,
                            0, 1, False, 33, byref(type_ret), byref(format_ret),
                            byref(nitems_ret), byref(bytes_after_ret), byref(winp))
        if not fail and format_ret.value == 32 and nitems_ret.value == 1:
            return winp.contents.value

    def Close(self):
        self.loop_break = True
        self.loop_event.set()
        while self.isAlive():
            time.sleep(0.01)
        self.DebugPrint('closed')

    def SetFriendlyName(self, FriendlyName):
        self.FriendlyName = FriendlyName
        if self.AttachmentStatus == apiAttachSuccess:
            # reattach with the new name
            self.SetAttachmentStatus(apiAttachUnknown)
            self.Attach()

    def __Attach_ftimeout(self):
        self.wait = False

    def Attach(self, Timeout=30000, Wait=True):
        if self.AttachmentStatus == apiAttachSuccess:
            return
        if not self.isAlive():
            try:
                self.start()
            except AssertionError:
                raise ISkypeAPIError('Skype API closed')
        try:
            self.wait = True
            t = threading.Timer(Timeout / 1000.0, self.__Attach_ftimeout)
            if Wait:
                t.start()
            while self.wait:
                self.win_skype = self.get_skype()
                if self.win_skype is not None:
                    break
                else:
                    time.sleep(1.0)
            else:
                raise ISkypeAPIError('Skype attach timeout')
        finally:
            t.cancel()
        c = ICommand(-1, 'NAME %s' % self.FriendlyName, '', True, Timeout)
        self.SendCommand(c, True)
        if c.Reply != 'OK':
            self.win_skype = None
            self.SetAttachmentStatus(apiAttachRefused)
            return
        self.SendCommand(ICommand(-1, 'PROTOCOL %s' % self.Protocol), True)
        self.SetAttachmentStatus(apiAttachSuccess)

    def IsRunning(self):
        return self.get_skype() is not None

    def Start(self, Minimized=False, Nosplash=False):
        # options are not supported as of Skype 1.4 Beta for Linux
        if not self.IsRunning():
            import os
            if os.fork() == 0: # we're the child
                os.setsid()
                os.execlp('skype')

    def Shutdown(self):
        import os
        from signal import SIGINT
        fh = os.popen('ps -o %p --no-heading -C skype')
        pid = fh.readline().strip()
        fh.close()
        if pid:
            os.kill(int(pid), SIGINT)
            # Skype sometimes doesn't delete the '_SKYPE_INSTANCE' property
            skype_inst = _x11.XInternAtom(self.disp, '_SKYPE_INSTANCE', True)
            if skype_inst:
                _x11.XDeleteProperty(self.disp, self.win_root, skype_inst)
            self.win_skype = None
            self.SetAttachmentStatus(apiAttachNotAvailable)

    def SendCommand(self, Command, Force=False):
        if self.AttachmentStatus != apiAttachSuccess and not Force:
            self.Attach(Command.Timeout)
        self.CommandsStackPush(Command)
        self.CallHandler('send', Command)
        com = u'#%d %s' % (Command.Id, Command.Command)
        self.DebugPrint('->', repr(com))
        if Command.Blocking:
            Command._event = bevent = threading.Event()
        else:
            Command._timer = timer = threading.Timer(Command.Timeout / 1000.0, self.CommandsStackPop, (Command.Id,))
        event = _XEvent()
        event.xclient.type = _ClientMessage
        event.xclient.display = self.disp
        event.xclient.window = self.win_self
        event.xclient.message_type = self.atom_msg_begin
        event.xclient.format = 8
        com = com.encode('utf-8') + '\x00'
        for i in xrange(0, len(com), 20):
            event.xclient.data = com[i:i+20]
            _x11.XSendEvent(self.disp, self.win_skype, False, 0, byref(event))
            event.xclient.message_type = self.atom_msg
        self.loop_event.set()
        if Command.Blocking:
            bevent.wait(Command.Timeout / 1000.0)
            if not bevent.isSet():
                raise ISkypeAPIError('Skype command timeout')
        else:
            timer.start()

    def notify(self, com):
        self.DebugPrint('<-', repr(com))
        # Called by main loop for all received Skype commands.
        if com.startswith(u'#'):
            p = com.find(u' ')
            Command = self.CommandsStackPop(int(com[1:p]))
            if Command:
                Command.Reply = com[p + 1:]
                if Command.Blocking:
                    Command._event.set()
                    del Command._event
                else:
                    Command._timer.cancel()
                    del Command._timer
                self.CallHandler('rece', Command)
            else:
                self.CallHandler('rece_api', com[p + 1:])
        else:
            self.CallHandler('rece_api', com)

