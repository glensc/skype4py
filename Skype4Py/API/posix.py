'''
Low level Skype for Linux interface implemented using dbus module.

Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

import threading
import time
import dbus, dbus.mainloop.glib, dbus.service
import gobject
from Skype4Py.API import *
from Skype4Py.enums import *
from Skype4Py.errors import ISkypeAPIError


dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
gobject.threads_init()


class _SkypeNotify(dbus.service.Object):
    def __init__(self, bus, notify):
        dbus.service.Object.__init__(self, bus, '/com/Skype/Client', bus_name='com.Skype.API')
        self.notify = notify

    @dbus.service.method(dbus_interface='com.Skype.API')
    def Notify(self, com):
        self.notify(com)

class ISkypeAPI(ISkypeAPIBase):
    def __init__(self):
        ISkypeAPIBase.__init__(self)
        self.loop = None
        self.skype_in = self.skype_out = None
        self.bus = dbus.SessionBus()

    def run(self):
        self.loop = gobject.MainLoop()
        self.loop.run()

    def Close(self):
        if self.loop:
            self.loop.quit()
        self.skype_in = self.skype_out = None

    def SetFriendlyName(self, FriendlyName):
        self.FriendlyName = FriendlyName
        if self.skype_out:
            self.SendCommand(ICommand(-1, 'NAME %s' % FriendlyName))

    def Attach(self, Timeout):
        if self.skype_out:
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
                try:
                    self.skype_out = self.bus.get_object('com.Skype.API', '/com/Skype')
                    self.skype_in = _SkypeNotify(self.bus, self.notify)
                except dbus.DBusException:
                    time.sleep(1.0)
                else:
                    break
            else:
                raise ISkypeAPIError('Skype attach timeout')
        finally:
            t.cancel()
        while not self.loop:
            time.sleep(0.01)
        c = ICommand(-1, 'NAME %s' % self.FriendlyName, '', True, Timeout)
        self.SendCommand(c)
        if c.Reply != 'OK':
            self.skype_in = self.skype_out = None
            self.CallHandler('attach', apiAttachRefused)
            return
        self.SendCommand(ICommand(-1, 'PROTOCOL %s' % self.Protocol))
        self.CallHandler('attach', apiAttachSuccess)

    def IsRunning(self):
        try:
            self.bus.get_object('com.Skype.API', '/com/Skype')
            return True
        except dbus.DBusException:
            return False

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
        if not self.skype_out:
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
            result = self.skype_out.Invoke(com)
        except dbus.DBusException, err:
            raise ISkypeAPIError(str(err))
        if result.startswith(u'#%d ' % Command.Id):
            self.notify(result)
        if Command.Blocking:
            event.wait(Command.Timeout / 1000.0)
            if not event.isSet():
                raise ISkypeAPIError('Skype command timeout')
        else:
            timer.start()

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

