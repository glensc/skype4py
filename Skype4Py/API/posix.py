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


class XClientMessageEvent(Structure):
    _fields_ = [('type', c_int),
                ('serial', c_ulong),
                ('send_event', c_int),
                ('display', c_void_p),
                ('window', c_ulong),
                ('message_type', c_ulong),
                ('format', c_int),
                ('data', c_char * 20)]


class XEvent(Union):
    _fields_ = [('xclient', XClientMessageEvent),
                ('padding', c_char * 96)]


class XErrorEvent(Structure):
    _fields_ = [('type', c_int),
                ('display', c_void_p),
                ('resourceid', c_ulong),
                ('serial', c_ulong),
                ('error_code', c_ubyte),
                ('request_code', c_ubyte),
                ('minor_code', c_ubyte)]


XCodes = {0: 'Success',
          2: 'BadValue',
          3: 'BadWindow',
          5: 'BadAtom'}


XErrorHandler = CFUNCTYPE(c_int, c_void_p, POINTER(XErrorEvent))


class XSkypeError(Exception):
    pass
    

class XSkype(object):
    '''Lower level interface to send commands to Skype and receive responses.'''
    
    def __init__(self, notify):
        # initialize Xlib, display, window, atoms
        self.notify = notify
        libpath = find_library('X11')
        if not libpath:
            raise ImportError('Could not locate X11 library')
        self.x11 = cdll.LoadLibrary(libpath)
        self.error = None
        # callback has to be saved to keep reference to bound method
        self._error_handler_callback = XErrorHandler(self._error_handler)
        self.x11.XSetErrorHandler(self._error_handler_callback)
        self.x11.XOpenDisplay.restype = c_void_p
        self.disp = self.x11.XOpenDisplay(None)
        if not self.disp:
            raise XSkypeError('Could not open XDisplay')
        self.win_skype = None
        self.win_root = self.x11.XDefaultRootWindow(self.disp)
        self.win_self = self.x11.XCreateSimpleWindow(self.disp, self.win_root,
                                    100, 100, 100, 100, 1, 0, 0)
        ctrl = 'SKYPECONTROLAPI_MESSAGE'
        self.atom_msg = self.x11.XInternAtom(self.disp, ctrl, True)
        self.atom_msg_begin = self.x11.XInternAtom(self.disp, ctrl + '_BEGIN', True)
        self.atom_stop_loop = self.x11.XInternAtom(self.disp, 'STOP_LOOP', True)

    def __del__(self):
        # close display
        self.close()
        if hasattr(self, 'x11'):
            if hasattr(self, 'disp'):
                self.x11.XCloseDisplay(self.disp)

    def close(self):
        # destroy window
        if hasattr(self, 'win_self'):
            self.x11.XDestroyWindow(self.disp, self.win_self)

    def _error_handler(self, disp, error):
        # called from within Xlib when error occures
        self.error = error.contents.error_code
        return 0

    def error_check(self):
        '''Checks last Xlib error and raises an XSkypeError exception if needed.'''
        if self.error != None:
            error = XSkypeError('X11 error: %s' % XCodes.get(self.error, str(self.error)))
            self.error = None
            raise error

    def discover(self):
        '''Obtains Skype window ID and stores it for later use.'''
        self.win_skype = self.get_skype()
        return bool(self.win_skype)

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

    def send(self, cmd):
        '''Sends a command to Skype.'''
        if not self.win_skype:
            if not self.discover():
                raise XSkypeError('Cannot connect to Skype')
        event = XEvent()
        event.xclient.type = 33 # ClientMessage
        event.xclient.display = self.disp
        event.xclient.window = self.win_self
        event.xclient.message_type = self.atom_msg_begin
        event.xclient.format = 8
        cmd = unicode(cmd).encode('utf-8') + '\x00'
        for i in xrange(0, len(cmd) - 1, 20):
            event.xclient.data = cmd[i:i+20]
            self.x11.XSendEvent(self.disp, self.win_skype, True, 0, byref(event))
            event.xclient.message_type = self.atom_msg
        self.x11.XFlush(self.disp)
        self.error_check()
        
    def loop(self):
        '''Event handling, has to be run on a separate thread.'''
        event = XEvent()
        data = ''
        while True:
            self.x11.XNextEvent(self.disp, byref(event))
            if event.xclient.type == 33: # ClientMessage
                if event.xclient.message_type == self.atom_msg_begin:
                    data = event.xclient.data
                elif event.xclient.message_type == self.atom_msg:
                    data += event.xclient.data
                elif event.xclient.message_type == self.atom_stop_loop:
                    break
                if len(event.xclient.data) != 20:
                    self.notify(data.decode('utf-8'))

    def stop_loop(self):
        '''Breaks event handling loop running on a separate thread.'''
        event = XEvent()
        event.xclient.type = 33 # ClientMessage
        event.xclient.display = self.disp
        event.xclient.window = self.win_self
        event.xclient.message_type = self.atom_stop_loop
        event.xclient.format = 8
        self.x11.XSendEvent(self.disp, self.win_self, True, 0, byref(event))
        self.x11.XFlush(self.disp)


class ISkypeAPI(ISkypeAPIBase):
    '''Skype4Py API interface based on XSkype (Xlib).'''
    
    def __init__(self):
        ISkypeAPIBase.__init__(self)
        try:
            self.skype = XSkype(self.notify)
        except XSkypeError, error:
            raise ISkypeAPIError(str(error))
        
    def run(self):
        self.skype.loop()

    def Close(self):
        self.skype.stop_loop()
        while self.isAlive():
            time.sleep(0.01)
        
    def SetFriendlyName(self, FriendlyName):
        self.FriendlyName = FriendlyName
        if self.skype_out:
            self.SendCommand(ICommand(-1, 'NAME %s' % FriendlyName))

    def Attach(self, Timeout):
        if self.skype.win_skype:
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
            t.start()
            while self.wait:
                if self.skype.discover():
                    break
                else:
                    time.sleep(1.0)
            else:
                raise ISkypeAPIError('Skype attach timeout')
        finally:
            t.cancel()
        c = ICommand(-1, 'NAME %s' % self.FriendlyName, '', True, Timeout)
        self.SendCommand(c)
        if c.Reply != 'OK':
            self.skype.win_skype = None
            self.CallHandler('attach', apiAttachRefused)
            return
        self.SendCommand(ICommand(-1, 'PROTOCOL %s' % self.Protocol))
        self.CallHandler('attach', apiAttachSuccess)

    def IsRunning(self):
        return bool(self.skype.get_skype())

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

    def SendCommand(self, Command):
        if not self.skype.win_skype:
            self.Attach(Command.Timeout)
        if Command.Id < 0:
            Command.Id = 0
            while Command.Id in self.Commands:
                Command.Id += 1
        if Command.Id in self.Commands:
            raise ISkypeAPIError('Command Id conflict')
        self.CallHandler('send', Command)
        com = u'#%d %s' % (Command.Id, Command.Command)
        if Command.Blocking:
            Command._event = event = threading.Event()
        else:
            Command._timer = timer = threading.Timer(Command.Timeout / 1000.0, self.async_cmd_timeout, (Command.Id,))
        self.Commands[Command.Id] = Command
        try:
            self.skype.send(com)
            if Command.Blocking:
                event.wait(Command.Timeout / 1000.0)
                if not event.isSet():
                    self.skype.error_check()
                    raise ISkypeAPIError('Skype command timeout')
            else:
                timer.start()
        except XSkypeError, error:
            raise ISkypeAPIError(str(error))

    def async_cmd_timeout(self, cid):
        if cid in self.Commands:
            del self.Commands[cid]

    def notify(self, com):
        if com.startswith(u'#'):
            p = com.find(u' ')
            i = int(com[1:p])
            command = self.Commands[i]
            del self.Commands[i]
            command.Reply = com[p + 1:]
            if command.Blocking:
                command._event.set()
                del command._event
            else:
                command._timer.cancel()
                del command._timer
            self.CallHandler('rece_api', command.Reply)
            self.CallHandler('rece', command)
        else:
            self.CallHandler('rece_api', com)
            
