'''
Low level Skype for Linux interface implemented
using python-dbus package.

This module handles the options that you can pass to L{ISkype.__init__} for Linux machines
when the transport is set to DBus.

@newfield option: Option, Options

@option: C{Bus} DBus bus object as returned by python-dbus package.
If not specified, private session bus is used.
@option: C{MainLoop} DBus mainloop object. If not specified, default DBus mainloop is used.
@option: C{BusName} Skype DBus bus name. Defaults to 'com.Skype.API'.
'''

import threading
import time
import weakref
from Skype4Py.API import ICommand, _ISkypeAPIBase
from Skype4Py.enums import *
from Skype4Py.errors import ISkypeAPIError
from Skype4Py.utils import cndexp


try:
    import dbus, dbus.service
except ImportError:
    import sys
    if sys.argv == ['(imported)']:
        # we get here if we're building docs on windows, to let the module
        # import without exceptions, we import our faked dbus module
        from _faked_dbus import dbus
    else:
        raise


class _SkypeNotifyCallback(dbus.service.Object):
    '''DBus object which exports a Notify method. This will be called by Skype for all
    notifications with the notification string as a parameter. The Notify method of this
    class calls in turn the callable passed to the constructor.
    '''

    def __init__(self, bus, notify):
        dbus.service.Object.__init__(self, bus, '/com/Skype/Client')
        self.notify = notify

    @dbus.service.method(dbus_interface='com.Skype.API.Client')
    def Notify(self, com):
        self.notify(unicode(com))


class _ISkypeAPI(_ISkypeAPIBase):
    def __init__(self, handler, **opts):
        _ISkypeAPIBase.__init__(self)
        self.RegisterHandler(handler)
        self.skype_in = self.skype_out = self.dbus_name_owner_watch = None
        self.bus = opts.pop('Bus', None)
        try:
            mainloop = opts.pop('MainLoop')
            if self.bus != None:
                raise TypeError('Bus and MainLoop cannot be used at the same time!')
        except KeyError:
            import dbus.mainloop.glib
            import gobject
            gobject.threads_init()
            dbus.mainloop.glib.threads_init()
            mainloop = dbus.mainloop.glib.DBusGMainLoop()
            self.mainloop = gobject.MainLoop()
        if self.bus == None:
            self.bus = dbus.SessionBus(private=True, mainloop=mainloop)
        self.bus_name = opts.pop('BusName', 'com.Skype.API')
        if opts:
            raise TypeError('Unexpected parameters: %s' % ', '.join(opts.keys()))

    def run(self):
        if hasattr(self, 'mainloop'):
            self.mainloop.run()

    def Close(self):
        if hasattr(self, 'mainloop'):
            self.mainloop.quit()
        self.skype_in = self.skype_out = None
        if self.dbus_name_owner_watch != None:
            self.bus.remove_signal_receiver(self.dbus_name_owner_watch)
        self.dbus_name_owner_watch = None

    def SetFriendlyName(self, FriendlyName):
        self.FriendlyName = FriendlyName
        if self.skype_out:
            self.SendCommand(ICommand(-1, 'NAME %s' % FriendlyName))

    def Attach(self, Timeout=30000, Wait=True):
        if self.skype_out:
            return
        try:
            self.start()
        except AssertionError:
            pass
        try:
            self.wait = True
            def ftimeout():
                self.wait = False
            t = threading.Timer(Timeout / 1000.0, ftimeout)
            if Wait:
                t.start()
            while self.wait:
                try:
                    self.skype_out = self.bus.get_object(self.bus_name, '/com/Skype')
                    self.skype_in = _SkypeNotifyCallback(self.bus, self.notify)
                except dbus.DBusException:
                    time.sleep(1.0)
                else:
                    break
            else:
                raise ISkypeAPIError('Skype attach timeout')
        finally:
            t.cancel()
        self.dbus_name_owner_watch = self.bus.add_signal_receiver(self.dbus_name_owner_changed,
            'NameOwnerChanged',
            'org.freedesktop.DBus',
            'org.freedesktop.DBus',
            '/org/freedesktop/DBus',
            arg0='com.Skype.API')
        c = ICommand(-1, 'NAME %s' % self.FriendlyName, '', True, Timeout)
        self.SendCommand(c)
        if c.Reply != 'OK':
            self.skype_in = self.skype_out = None
            self.SetAttachmentStatus(apiAttachRefused)
            return
        self.SendCommand(ICommand(-1, 'PROTOCOL %s' % self.Protocol))
        self.SetAttachmentStatus(apiAttachSuccess)

    def IsRunning(self):
        try:
            self.bus.get_object(self.bus_name, '/com/Skype')
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
        self.CommandsStackPush(Command)
        self.CallHandler('send', Command)
        com = u'#%d %s' % (Command.Id, Command.Command)
        if Command.Blocking:
            Command._event = event = threading.Event()
        else:
            Command._timer = timer = threading.Timer(Command.Timeout / 1000.0, self.CommandsStackPop, (Command.Id,))
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

    def notify(self, com):
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

    def dbus_name_owner_changed(self, owned, old_owner, new_owner):
        self.SetAttachmentStatus(cndexp(new_owner == '',
            apiAttachNotAvailable,
            apiAttachAvailable))

