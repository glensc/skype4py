'''
Low level Skype for Linux interface implemented
using XWindows messaging. Uses direct Xlib calls
through ctypes module.

Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

import threading
from ctypes import *
from ctypes.util import find_library
import time
from Skype4Py.API import *
from Skype4Py.enums import *
from Skype4Py.errors import ISkypeAPIError


# some Xlib constants
PropertyChangeMask = 0x400000
PropertyNotify = 28
ClientMessage = 33
PropertyNewValue = 0
PropertyDelete = 1


# some Xlib structures
class XClientMessageEvent(Structure):
    _fields_ = [('type', c_int),
                ('serial', c_ulong),
                ('send_event', c_int),
                ('display', c_void_p),
                ('window', c_ulong),
                ('message_type', c_ulong),
                ('format', c_int),
                ('data', c_char * 20)]

class XPropertyEvent(Structure):
    _fields_ = [('type', c_int),
                ('serial', c_ulong),
                ('send_event', c_int),
                ('display', c_void_p),
                ('window', c_ulong),
                ('atom', c_ulong),
                ('time', c_int),
                ('state', c_int)]

class XErrorEvent(Structure):
    _fields_ = [('type', c_int),
                ('display', c_void_p),
                ('resourceid', c_ulong),
                ('serial', c_ulong),
                ('error_code', c_ubyte),
                ('request_code', c_ubyte),
                ('minor_code', c_ubyte)]

class XEvent(Union):
    _fields_ = [('type', c_int),
                ('xclient', XClientMessageEvent),
                ('xproperty', XPropertyEvent),
                ('xerror', XErrorEvent),
                ('padding', c_char * 96)]


# Xlib error handler type
XErrorHandler = CFUNCTYPE(c_int, c_void_p, POINTER(XErrorEvent))


class ISkypeAPI(ISkypeAPIBase):
    def __init__(self, handler, **opts):
        ISkypeAPIBase.__init__(self)
        self.RegisterHandler(handler)
        # initialize Xlib, display, window, atoms
        libpath = find_library('X11')
        if not libpath:
            raise ImportError('Could not locate X11 library')
        self.x11 = cdll.LoadLibrary(libpath)
        self.x11.XInitThreads()
        self.x11.XGetAtomName.restype = c_char_p
        self.error = None
        # callback has to be saved to keep reference to bound method
        self._error_handler_callback = XErrorHandler(self._error_handler)
        self.x11.XSetErrorHandler(self._error_handler_callback)
        self.x11.XOpenDisplay.restype = c_void_p
        self.disp = self.x11.XOpenDisplay(None)
        if not self.disp:
            raise ISkypeAPIError('Could not open XDisplay')
        self.win_root = self.x11.XDefaultRootWindow(self.disp)
        self.win_self = self.x11.XCreateSimpleWindow(self.disp, self.win_root,
                                    100, 100, 100, 100, 1, 0, 0)
        self.x11.XSelectInput(self.disp, self.win_root, PropertyChangeMask)
        self.win_skype = self.get_skype()
        ctrl = 'SKYPECONTROLAPI_MESSAGE'
        self.atom_msg = self.x11.XInternAtom(self.disp, ctrl, True)
        self.atom_msg_begin = self.x11.XInternAtom(self.disp, ctrl + '_BEGIN', True)
        self.atom_stop_loop = self.x11.XInternAtom(self.disp, 'STOP_LOOP', True)

    def __del__(self):
        if hasattr(self, 'x11'):
            if hasattr(self, 'disp'):
                if hasattr(self, 'win_self'):
                    self.x11.XDestroyWindow(self.disp, self.win_self)
                self.x11.XCloseDisplay(self.disp)

    def run(self):
        # main loop
        event = XEvent()
        data = ''
        while True:
            self.x11.XNextEvent(self.disp, byref(event))
            if event.type == ClientMessage:
                if event.xclient.message_type == self.atom_msg_begin:
                    data = event.xclient.data
                elif event.xclient.message_type == self.atom_msg:
                    data += event.xclient.data
                elif event.xclient.message_type == self.atom_stop_loop:
                    break
                if len(event.xclient.data) != 20:
                    if data:
                        self.notify(data.decode('utf-8'))
            elif event.type == PropertyNotify:
                if self.x11.XGetAtomName(self.disp, event.xproperty.atom) == '_SKYPE_INSTANCE':
                    if event.xproperty.state == PropertyNewValue:
                        self.win_skype = self.get_skype()
                        # changing attachment status can cause an event handler to be fired, in
                        # turn it could try to call Attach() and doing this immediately seems to
                        # confuse Skype (command '#0 NAME xxx' returns '#0 CONNSTATUS OFFLINE' :D);
                        # to fix this, we give Skype some time to initialize itself
                        time.sleep(1.0)
                        self.SetAttachmentStatus(apiAttachAvailable)
                    elif event.xproperty.state == PropertyDelete:
                        self.win_skype = None
                        self.SetAttachmentStatus(apiAttachNotAvailable)

    def _error_handler(self, disp, error):
        # called from within Xlib when error occures
        self.error = error.contents.error_code
        # stop all pending commands
        for command in self.Commands.values():
            if hasattr(command, '_event'):
                command._event.set()
        return 0

    def error_check(self):
        '''Checks last Xlib error and raises an exception if needed.'''
        if self.error != None:
            if self.error == 3: # BadWindow
                self.win_skype = None
                self.SetAttachmentStatus(apiAttachNotAvailable)
            buf = create_string_buffer(256)
            self.x11.XGetErrorText(self.disp, self.error, buf, 256)
            error = ISkypeAPIError('X11 error: %s' % buf.value)
            self.error = None
            raise error

    def get_skype(self):
        '''Returns Skype window ID or None if Skype not running.'''
        skype_inst = self.x11.XInternAtom(self.disp, '_SKYPE_INSTANCE', False)
        type_ret = c_ulong()
        format_ret = c_int()
        nitems_ret = c_ulong()
        bytes_after_ret = c_ulong()
        prop = pointer(c_ulong())
        fail = self.x11.XGetWindowProperty(self.disp, self.win_root, skype_inst,
                            0, 1, False, 33, byref(type_ret), byref(format_ret),
                            byref(nitems_ret), byref(bytes_after_ret), byref(prop))
        if not fail and self.error == None and format_ret.value == 32 and nitems_ret.value == 1:
            return prop.contents.value

    def Close(self):
        event = XEvent()
        event.xclient.type = ClientMessage
        event.xclient.display = self.disp
        event.xclient.window = self.win_self
        event.xclient.message_type = self.atom_stop_loop
        event.xclient.format = 8
        self.x11.XSendEvent(self.disp, self.win_self, True, 0, byref(event))
        self.x11.XFlush(self.disp)
        while self.isAlive():
            time.sleep(0.01)

    def SetFriendlyName(self, FriendlyName):
        self.FriendlyName = FriendlyName
        if self.AttachmentStatus == apiAttachSuccess:
            # reattach with the new name
            self.SetAttachmentStatus(apiAttachUnknown)
            self.Attach()

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
            def ftimeout():
                self.wait = False
            t = threading.Timer(Timeout / 1000.0, ftimeout)
            if Wait:
                t.start()
            while self.wait:
                self.win_skype = self.get_skype()
                if self.win_skype != None:
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
        return bool(self.get_skype())

    def Start(self, Minimized=False, Nosplash=False):
        # options are not supported as of Skype 1.4 Beta for Linux
        if not self.IsRunning():
            import os
            if os.fork() == 0: # we're child
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
            self.skype_in = self.skype_out = None

    def SendCommand(self, Command, Force=False):
        if self.AttachmentStatus != apiAttachSuccess and not Force:
            self.Attach(Command.Timeout)
        self.CommandsStackPush(Command)
        self.CallHandler('send', Command)
        com = u'#%d %s' % (Command.Id, Command.Command)
        if Command.Blocking:
            Command._event = bevent = threading.Event()
        else:
            Command._timer = timer = threading.Timer(Command.Timeout / 1000.0, self.CommandsStackPop, (Command.Id,))
        event = XEvent()
        event.xclient.type = 33 # ClientMessage
        event.xclient.display = self.disp
        event.xclient.window = self.win_self
        event.xclient.message_type = self.atom_msg_begin
        event.xclient.format = 8
        com = unicode(com).encode('utf-8') + '\x00'
        for i in xrange(0, len(com), 20):
            event.xclient.data = com[i:i+20]
            self.x11.XSendEvent(self.disp, self.win_skype, True, 0, byref(event))
            event.xclient.message_type = self.atom_msg
        self.x11.XFlush(self.disp)
        self.error_check()
        if Command.Blocking:
            bevent.wait(Command.Timeout / 1000.0)
            self.error_check()
            if not bevent.isSet():
                raise ISkypeAPIError('Skype command timeout')
        else:
            timer.start()

    def notify(self, com):
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
                if not Command.Command.startswith('GET '):
                    self.CallHandler('rece_api', Command.Reply)
                self.CallHandler('rece', Command)
            else:
                self.CallHandler('rece_api', com[p + 1:])
        else:
            self.CallHandler('rece_api', com)

