'''
Low level Skype for Windows interface implemented
using Windows messaging. Uses direct WinAPI calls
through ctypes module.

Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

import threading
import time
import weakref
from ctypes import *
from Skype4Py.API import *
from Skype4Py.errors import ISkypeAPIError


WNDPROC = WINFUNCTYPE(c_long, c_int, c_uint, c_int, c_int)

class WNDCLASS(Structure):
    _fields_ = [('style', c_uint),
                ('lpfnWndProc', WNDPROC),
                ('cbClsExtra', c_int),
                ('cbWndExtra', c_int),
                ('hInstance', c_int),
                ('hIcon', c_int),
                ('hCursor', c_int),
                ('hbrBackground', c_int),
                ('lpszMenuName', c_char_p),
                ('lpszClassName', c_char_p)]


class MSG(Structure):
    _fields_ = [('hwnd', c_int),
                ('message', c_uint),
                ('wParam', c_int),
                ('lParam', c_int),
                ('time', c_int),
                ('pointX', c_long),
                ('pointY', c_long)]


class COPYDATASTRUCT(Structure):
    _fields_ = [('dwData', POINTER(c_uint)),
                ('cbData', c_uint),
                ('lpData', c_char_p)]
PCOPYDATASTRUCT = POINTER(COPYDATASTRUCT)

WM_QUIT = 0x12
WM_COPYDATA = 0x4A

HWND_BROADCAST = 0xFFFF

SkypeControlAPIDiscover = windll.user32.RegisterWindowMessageA('SkypeControlAPIDiscover')
SkypeControlAPIAttach = windll.user32.RegisterWindowMessageA('SkypeControlAPIAttach')


class ISkypeAPI(ISkypeAPIBase):
    def __init__(self, handler, **opts):
        ISkypeAPIBase.__init__(self)
        self.hwnd = None
        self.Skype = None
        self.RegisterHandler(handler)

    def run(self):
        if not self.CreateWindow():
            self.hwnd = None
            return

        Msg = MSG()
        pMsg = pointer(Msg)
        while self.hwnd and windll.user32.GetMessageA(pMsg, self.hwnd, 0, 0):
            windll.user32.TranslateMessage(pMsg)
            windll.user32.DispatchMessageA(pMsg)

        self.DestroyWindow()
        self.hwnd = None

    def Close(self):
        # if there are no active handlers
        if self.NumOfHandlers() == 0:
            if self.hwnd:
                windll.user32.PostMessageA(self.hwnd, WM_QUIT, 0, 0)
                while self.hwnd:
                    time.sleep(0.01)
            self.Skype = None

    def SetFriendlyName(self, FriendlyName):
        self.FriendlyName = FriendlyName
        if self.Skype:
            self.SendCommand(ICommand(-1, 'NAME %s' % FriendlyName))

    def Attach(self, Timeout):
        if self.Skype:
            return
        if not self.isAlive():
            try:
                self.start()
            except AssertionError:
                raise ISkypeAPIError('Skype API closed')
            # wait till the thread initializes
            while not self.hwnd:
                time.sleep(0.01)
        if not windll.user32.SendMessageTimeoutA(HWND_BROADCAST, SkypeControlAPIDiscover,
                                                 self.hwnd, None, 2, 5000, None):
            raise ISkypeAPIError('Could not broadcast Skype discover message')
        # wait (with timeout) till the WindProc() attaches
        self.Wait = True
        def ftimeout():
            self.Wait = False
        t = threading.Timer(Timeout / 1000, ftimeout)
        t.start()
        while self.Wait and self.AttachmentStatus not in [apiAttachSuccess, apiAttachRefused]:
            if self.AttachmentStatus == apiAttachPendingAuthorization:
                # disable the timeout
                t.cancel()
            elif self.AttachmentStatus == apiAttachAvailable:
                # rebroadcast
                if not windll.user32.SendMessageTimeoutA(HWND_BROADCAST, SkypeControlAPIDiscover,
                                                         self.hwnd, None, 2, 5000, None):
                    raise ISkypeAPIError('Could not broadcast Skype discover message')
            time.sleep(0.01)
        t.cancel()
        # check if we got the Skype window's hwnd
        if self.Skype:
            self.SendCommand(ICommand(-1, 'PROTOCOL %s' % self.Protocol))
        elif not self.Wait:
            raise ISkypeAPIError('Skype attach timeout')

    def IsRunning(self):
        return bool(windll.user32.FindWindowA('SkypeWindowClass2', None))

    def get_skype_path(self):
        key = c_long()
        # try to find Skype in HKEY_CURRENT_USER registry tree
        if windll.advapi32.RegOpenKeyA(0x80000001, 'Software\\Skype\\Phone', byref(key)) != 0:
            # try to find Skype in HKEY_LOCAL_MACHINE registry tree
            if windll.advapi32.RegOpenKeyA(0x80000002, 'Software\\Skype\\Phone', byref(key)) != 0:
                raise ISkypeAPIError('Skype not installed')
        pathlen = c_long(512)
        path = create_string_buffer(pathlen.value)
        if windll.advapi32.RegQueryValueExA(key, 'SkypePath', None, None, path, byref(pathlen)) != 0:
            windll.advapi32.RegCloseKey(key)
            raise ISkypeAPIError('Cannot find Skype path')
        windll.advapi32.RegCloseKey(key)
        return path.value

    def Start(self, Minimized=False, Nosplash=False):
        args = []
        if Minimized:
            args.append('/MINIMIZED')
        if Nosplash:
            args.append('/NOSPLASH')
        if windll.shell32.ShellExecuteA(None, 'open', self.get_skype_path(), ' '.join(args), None, 0) <= 32:
            raise ISkypeAPIError('Could not start Skype')

    def Shutdown(self):
        if windll.shell32.ShellExecuteA(None, 'open', self.get_skype_path(), '/SHUTDOWN', None, 0) <= 32:
            raise ISkypeAPIError('Could not shutdown Skype')

    def CreateWindow(self):
        # window class has to be saved as property to keep reference to self.WinProc
        self.window_class = WNDCLASS(3, WNDPROC(self.WinProc), 0, 0,
                                     windll.kernel32.GetModuleHandleA(None),
                                     0, 0, 0, None, 'Skype4Py.%d' % id(self))

        wclass = windll.user32.RegisterClassA(byref(self.window_class))
        if wclass == 0:
            return False

        self.hwnd = windll.user32.CreateWindowExA(0, 'Skype4Py.%d' % id(self), 'Skype4Py',
                                                  0xCF0000, 0x80000000, 0x80000000,
                                                  0x80000000, 0x80000000, None, None,
                                                  self.window_class.hInstance, None)
        if self.hwnd == 0:
            windll.user32.UnregisterClassA('Skype4Py.%d' % id(self), None)
            return False

        return True

    def DestroyWindow(self):
        if not windll.user32.DestroyWindow(self.hwnd):
            return False

        if not windll.user32.UnregisterClassA('Skype4Py.%d' % id(self), None):
            return False

        return True

    def WinProc(self, hwnd, uMsg, wParam, lParam):
        if uMsg == SkypeControlAPIAttach:
            if lParam == apiAttachSuccess:
                self.Skype = wParam
            elif lParam in [apiAttachRefused, apiAttachNotAvailable, apiAttachAvailable]:
                self.Skype = None
            self.SetAttachmentStatus(lParam)
            return 1
        elif uMsg == WM_COPYDATA and wParam == self.Skype and lParam:
            copydata = cast(lParam, PCOPYDATASTRUCT).contents
            com8 = copydata.lpData[:copydata.cbData - 1]
            com = com8.decode('utf-8')
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
                    self.CallHandler('rece_api', Command.Reply)
                    self.CallHandler('rece', Command)
                else:
                    self.CallHandler('rece_api', com[p + 1:])
            else:
                self.CallHandler('rece_api', com)
            return 1
        return windll.user32.DefWindowProcA(c_int(hwnd), c_int(uMsg), c_int(wParam), c_int(lParam))

    def SendCommand(self, Command):
        if not self.Skype:
            self.Attach(Command.Timeout)
        self.CommandsStackPush(Command)
        self.CallHandler('send', Command)
        com = u'#%d %s' % (Command.Id, Command.Command)
        com8 = com.encode('utf-8') + '\0'
        copydata = COPYDATASTRUCT(None, len(com8), com8)
        if Command.Blocking:
            Command._event = event = threading.Event()
        else:
            Command._timer = timer = threading.Timer(Command.Timeout / 1000.0, self.CommandsStackPop, (Command.Id,))
        if windll.user32.SendMessageA(self.Skype, WM_COPYDATA, self.hwnd, byref(copydata)):
            if Command.Blocking:
                event.wait(Command.Timeout / 1000.0)
                if not event.isSet():
                    raise ISkypeAPIError('Skype command timeout')
            else:
                timer.start()
        else:
            raise ISkypeAPIError('Skype API error, check if Skype wasn\'t closed')

