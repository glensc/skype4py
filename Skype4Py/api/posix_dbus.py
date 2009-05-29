'''
Low level *Skype for Linux* interface implemented using *python-dbus* package.

This module handles the options that you can pass to `Skype.__init__`
for Linux machines when the transport is set to *DBus*. See below.

- ``Bus`` (``dbus.Bus``) - DBus bus object as returned by python-dbus package.
  If not specified, private session bus is created and used. See also the
  ``MainLoop`` option.
  
- ``MainLoop`` - DBus mainloop object. Use only without specifying the ``Bus``
  option (if you need, pass the mainloop object to the bus constructor). If
  neither ``Bus`` or ``MainLoop`` are specified, glib mainloop is used. In such
  case, the mainloop is automatically run on a separate thread upon attaching
  to the Skype client. If you want to use glib mainloop but you want to run the
  loop yourself (for example because your GUI toolkit does it for you, like
  *PyGTK* does), pass the ``dbus.mainloop.glib.DBusGMainLoop`` object as the
  ``MainLoop`` option.

:requires: Skype for Linux 2.0 (beta) or newer.
'''
__docformat__ = 'restructuredtext en'


import sys
import threading
import time
import logging

from Skype4Py.api import Command, SkypeAPIBase, timeout2float
from Skype4Py.enums import *
from Skype4Py.errors import SkypeAPIError
from Skype4Py.utils import cndexp


__all__ = ['SkypeAPI']


if getattr(sys, 'skype4py_setup', False):
    # we get here if we're building docs; to let the module import without
    # exceptions, we emulate the dbus module using a class:
    class dbus(object):
        class service(object):
            class Object(object):
                pass
            @staticmethod
            def method(*args, **kwargs):
                return lambda *args, **kwargs: None
else:
    import dbus, dbus.service


class SkypeNotifyCallback(dbus.service.Object):
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


class SkypeAPI(SkypeAPIBase):
    def __init__(self, opts):
        self.logger = logging.getLogger('Skype4Py.api.posix_dbus.SkypeAPI')
        SkypeAPIBase.__init__(self, opts)
        self.skype_in = self.skype_out = self.dbus_name_owner_watch = None
        self.bus = opts.pop('Bus', None)
        try:
            mainloop = opts.pop('MainLoop')
            if self.bus is not None:
                raise TypeError('Bus and MainLoop cannot be used at the same time!')
        except KeyError:
            if self.bus is None:
                import dbus.mainloop.glib
                import gobject
                gobject.threads_init()
                dbus.mainloop.glib.threads_init()
                mainloop = dbus.mainloop.glib.DBusGMainLoop()
                self.mainloop = gobject.MainLoop()
        if self.bus is None:
            from dbus import SessionBus
            self.bus = SessionBus(private=True, mainloop=mainloop)
        self.finalize_opts(opts)

    def run(self):
        self.logger.info('thread started')
        if hasattr(self, 'mainloop'):
            self.mainloop.run()
        self.logger.info('thread finished')

    def close(self):
        if hasattr(self, 'mainloop'):
            self.mainloop.quit()
        self.skype_in = self.skype_out = None
        if self.dbus_name_owner_watch is not None:
            self.bus.remove_signal_receiver(self.dbus_name_owner_watch)
        self.dbus_name_owner_watch = None
        SkypeAPIBase.close(self)

    def set_friendly_name(self, friendly_name):
        SkypeAPIBase.set_friendly_name(self, friendly_name)
        if self.skype_out:
            self.send_command(Command('NAME %s' % friendly_name))

    def start_watcher(self):
        self.dbus_name_owner_watch = self.bus.add_signal_receiver(self.dbus_name_owner_changed,
            'NameOwnerChanged',
            'org.freedesktop.DBus',
            'org.freedesktop.DBus',
            '/org/freedesktop/DBus',
            arg0='com.Skype.API')

    def attach(self, timeout, wait=True):
        self.acquire()
        try:
            try:
                if not self.isAlive():
                    self.start_watcher()
                    self.start()
            except AssertionError:
                pass
            try:
                self.wait = True
                t = threading.Timer(timeout2float(timeout), lambda: setattr(self, 'wait', False))
                if wait:
                    t.start()
                while self.wait:
                    if not wait:
                        self.wait = False
                    try:
                        if not self.skype_out:
                            self.skype_out = self.bus.get_object('com.Skype.API', '/com/Skype')
                        if not self.skype_in:
                            self.skype_in = SkypeNotifyCallback(self.bus, self.notify)
                    except dbus.DBusException:
                        if not wait:
                            break
                        time.sleep(1.0)
                    else:
                        break
                else:
                    raise SkypeAPIError('Skype attach timeout')
            finally:
                t.cancel()
            command = Command('NAME %s' % self.friendly_name, '', True, timeout)
            if self.skype_out:
                self.release()
                try:
                    self.send_command(command)
                finally:
                    self.acquire()
            if command.Reply != 'OK':
                self.skype_out = None
                self.set_attachment_status(apiAttachRefused)
                return
            self.send_command(Command('PROTOCOL %s' % self.protocol))
            self.set_attachment_status(apiAttachSuccess)
        finally:
            self.release()

    def is_running(self):
        try:
            self.bus.get_object('com.Skype.API', '/com/Skype')
            return True
        except dbus.DBusException:
            return False

    def startup(self, minimized, nosplash):
        # options are not supported as of Skype 1.4 Beta for Linux
        if not self.is_running():
            import os
            if os.fork() == 0: # we're child
                os.setsid()
                os.execlp('skype')

    def shutdown(self):
        import os
        from signal import SIGINT
        fh = os.popen('ps -o %p --no-heading -C skype')
        pid = fh.readline().strip()
        fh.close()
        if pid:
            os.kill(int(pid), SIGINT)
            self.skype_in = self.skype_out = None

    def send_command(self, command):
        if not self.skype_out:
            self.attach(command.Timeout)
        self.push_command(command)
        self.notifier.sending_command(command)
        cmd = u'#%d %s' % (command.Id, command.Command)
        self.logger.debug('sending %s', repr(cmd))
        if command.Blocking:
            command._event = event = threading.Event()
        else:
            command._timer = timer = threading.Timer(command.timeout2float(), self.pop_command, (command.Id,))
        try:
            result = self.skype_out.Invoke(cmd)
        except dbus.DBusException, err:
            raise SkypeAPIError(str(err))
        if result.startswith(u'#%d ' % command.Id):
            self.notify(result)
        if command.Blocking:
            event.wait(command.timeout2float())
            if not event.isSet():
                raise SkypeAPIError('Skype command timeout')
        else:
            timer.start()

    def notify(self, cmd):
        self.logger.debug('received %s', repr(cmd))
        if cmd.startswith(u'#'):
            p = cmd.find(u' ')
            command = self.pop_command(int(cmd[1:p]))
            if command is not None:
                command.Reply = cmd[p + 1:]
                if command.Blocking:
                    command._event.set()
                    del command._event
                else:
                    command._timer.cancel()
                    del command._timer
                self.notifier.reply_received(command)
            else:
                self.notifier.notification_received(cmd[p + 1:])
        else:
            self.notifier.notification_received(cmd)

    def dbus_name_owner_changed(self, owned, old_owner, new_owner):
        self.logger.debug('received dbus name owner changed')
        if new_owner == '':
            self.skype_out = None
        self.set_attachment_status(cndexp((new_owner == ''),
            apiAttachNotAvailable,
            apiAttachAvailable))
