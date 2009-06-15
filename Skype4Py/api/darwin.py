'''
Low level *Skype for Mac OS X* interface implemented using *Carbon
distributed notifications*. Uses direct *Carbon*/*CoreFoundation*
calls through the *ctypes* module.

This module handles the options that you can pass to
`Skype.__init__` for *Mac OS X* machines.

No further options are currently supported.

Thanks to **Eion Robb** for reversing *Skype for Mac* API protocol.
'''
__docformat__ = 'restructuredtext en'


import sys
from ctypes import *
from ctypes.util import find_library
import threading
import time
import logging

from Skype4Py.api import Command, SkypeAPIBase, \
                         timeout2float, finalize_opts
from Skype4Py.errors import SkypeAPIError
from Skype4Py.enums import *


__all__ = ['SkypeAPI']


class Carbon(object):
    '''Represents the Carbon.framework.
    '''

    def __init__(self):
        path = find_library('Carbon')
        if path is None:
            raise ImportError('Could not find Carbon.framework')
        self.lib = cdll.LoadLibrary(path)
        self.lib.RunCurrentEventLoop.argtypes = (c_double,)

    def RunCurrentEventLoop(self, timeout=-1):
        # timeout=-1 means forever
        return self.lib.RunCurrentEventLoop(timeout)

    def GetCurrentEventLoop(self):
        return EventLoop(c_void_p(self.lib.GetCurrentEventLoop()))


class EventLoop(object):
    '''Represents an EventLoop from Carbon.framework.

    :see: http://developer.apple.com/documentation/Carbon/Reference/Carbon_Event_Manager_Ref/
    '''

    def __init__(self, handle):
        self.handle = handle

    def quit(self):
        carbon.lib.QuitEventLoop(self.handle)


class CoreFoundation(object):
    '''Represents the CoreFoundation.framework.
    '''

    def __init__(self):
        path = find_library('CoreFoundation')
        if path is None:
            raise ImportError('Could not find CoreFoundation.framework')
        self.lib = cdll.LoadLibrary(path)
        self.strs = []

    def CFSTR(self, s):
        s = unicode(s)
        for cfs in self.strs:
            if unicode(cfs) == s:
                return cfs
        cfs = CFString(s)
        self.strs.append(cfs)
        return cfs


class CFType(object):
    '''Fundamental type for all CoreFoundation types.

    :see: http://developer.apple.com/documentation/CoreFoundation/Reference/CFTypeRef/
    '''

    def __init__(self, cast=None):
        self.handle = None
        self.owner = False
        if cast is not None:
            if isinstance(cast, CFType):
                self.handle = cast.get_handle()
            elif isinstance(cast, c_void_p):
                self.handle = cast
            elif isinstance(cast, (int, long)):
                self.handle = c_void_p(cast)
            else:
                raise TypeError('illegal cast type: %s' % type(cast))

    def retain(self):
        if not self.owner:
            core.lib.CFRetain(self)
            self.owner = True

    def is_owner(self):
        return not not self.owner

    def get_handle(self):
        return self.handle

    def __del__(self):
        if self.owner:
            core.lib.CFRelease(self)
        self.handle = None

    def __repr__(self):
        return '%s(handle=%s)' % (self.__class__.__name__, repr(self.handle))

    # allows passing CF types as ctypes function parameters
    _as_parameter_ = property(get_handle)


class CFString(CFType):
    '''CoreFoundation string type.

    Supports Python unicode type only. String is immutable.

    :see: http://developer.apple.com/documentation/CoreFoundation/Reference/CFStringRef/
    '''

    def __init__(self, cast):
        if isinstance(cast, (str, unicode)):
            CFType.__init__(self)
            s = unicode(cast).encode('utf-8')
            self.handle = c_void_p(core.lib.CFStringCreateWithBytes(None,
                s, len(s), 0x08000100, False))
            self.owner = True
        else:
            CFType.__init__(self, cast)

    def __str__(self):
        i = core.lib.CFStringGetLength(self)
        size = c_long()
        if core.lib.CFStringGetBytes(self, 0, i, 0x08000100, 0, False, None, 0, byref(size)) > 0:
            buf = create_string_buffer(size.value)
            core.lib.CFStringGetBytes(self, 0, i, 0x08000100, 0, False, buf, size, None)
            return buf.value
        else:
            raise UnicodeError('CFStringGetBytes() failed')

    def __unicode__(self):
        return self.__str__().decode('utf-8')

    def __len__(self):
        return core.lib.CFStringGetLength(self)

    def __repr__(self):
        return 'CFString(%s)' % repr(unicode(self))


class CFNumber(CFType):
    '''CoreFoundation number type.

    Supports Python int type only. Number is immutable.

    :see: http://developer.apple.com/documentation/CoreFoundation/Reference/CFNumberRef/
    '''

    def __init__(self, cast):
        if isinstance(cast, (int, long)):
            CFType.__init__(self)
            self.handle = c_void_p(core.lib.CFNumberCreate(None, 3, byref(c_int(int(cast)))))
            self.owner = True
        else:
            CFType.__init__(self, cast)

    def __int__(self):
        n = c_int()
        if core.lib.CFNumberGetValue(self, 3, byref(n)):
            return n.value
        return 0

    def __repr__(self):
        return 'CFNumber(%s)' % repr(int(self))


class CFDictionary(CFType):
    '''CoreFoundation immutable dictionary type.

    :see: http://developer.apple.com/documentation/CoreFoundation/Reference/CFDictionaryRef/
    '''

    def __init__(self, cast):
        if isinstance(cast, dict):
            CFType.__init__(self)
            d = dict(cast)
            keys = (c_void_p * len(d))()
            values = (c_void_p * len(d))()
            for i, (k, v) in enumerate(d.items()):
                keys[i] = k.get_handle()
                values[i] = v.get_handle()
            self.handle = c_void_p(core.lib.CFDictionaryCreate(None, keys, values, len(d),
                core.lib.kCFTypeDictionaryKeyCallBacks, core.lib.kCFTypeDictionaryValueCallBacks))
            self.owner = True
        else:
            CFType.__init__(self, cast)

    def get_dict(self):
        n = len(self)
        keys = (c_void_p * n)()
        values = (c_void_p * n)()
        core.lib.CFDictionaryGetKeysAndValues(self, keys, values)
        d = dict()
        for i in xrange(n):
            d[core.CFType(keys[i])] = core.CFType(values[i])
        return d

    def __getitem__(self, key):
        return core.CFType(c_void_p(core.lib.CFDictionaryGetValue(self, key)))

    def __len__(self):
        return core.lib.CFDictionaryGetCount(self)


class CFDistributedNotificationCenter(CFType):
    '''CoreFoundation distributed notification center type.

    :see: http://developer.apple.com/documentation/CoreFoundation/Reference/CFNotificationCenterRef/
    '''

    CFNotificationCallback = CFUNCTYPE(None, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p)

    def __init__(self):
        CFType.__init__(self)
        self.handle = c_void_p(core.lib.CFNotificationCenterGetDistributedCenter())
        # there is only one distributed notification center per application, every
        # call to the above function returns the same object so we're not owning it
        self.owner = False
        self.callbacks = {}
        self._callback = self.CFNotificationCallback(self._notification_callback)

    def _notification_callback(self, center, observer, name, obj, userInfo):
        observer = CFString(observer)
        name = CFString(name)
        if obj:
            obj = CFString(obj)
        callback = self.callbacks[(unicode(observer), unicode(name))]
        callback(self, observer, name, obj, CFDictionary(userInfo))

    def add_observer(self, observer, callback, name=None, obj=None,
            drop=False, coalesce=False, hold=False, immediate=False):
        if not isinstance(observer, CFString):
            observer = CFString(observer)
        if not callable(callback):
            raise TypeError('callback must be callable')
        self.callbacks[(unicode(observer), unicode(name))] = callback
        if name is not None and not isinstance(name, CFString):
            name = core.CFSTR(name)
        if obj is not None and not isinstance(obj, CFString):
            obj = core.CFSTR(obj)
        if drop:
            behaviour = 1
        elif coalesce:
            behaviour = 2
        elif hold:
            behaviour = 3
        elif immediate:
            behaviour = 4
        else:
            behaviour = 0
        core.lib.CFNotificationCenterAddObserver(self, observer, self._callback,
            name, obj, behaviour)

    def remove_observer(self, observer, name=None, obj=None):
        if not isinstance(observer, CFString):
            observer = CFString(observer)
        if name is not None and not isinstance(name, CFString):
            name = core.CFSTR(name)
        if obj is not None and not isinstance(obj, CFString):
            obj = core.CFSTR(obj)
        core.lib.CFNotificationCenterRemoveObserver(self, observer, name, obj)
        try:
            del self.callbacks[(unicode(observer), unicode(name))]
        except KeyError:
            pass

    def post_notification(self, name, obj=None, userInfo=None, immediate=False):
        if not isinstance(name, CFString):
            name = core.CFSTR(name)
        if obj is not None and not isinstance(obj, CFString):
            obj = core.CFSTR(obj)
        if userInfo is not None and not isinstance(userInfo, CFDictionary):
            userInfo = CFDictionary(userInfo)
        core.lib.CFNotificationCenterPostNotification(self, name, obj, userInfo, immediate)


# create the Carbon and CoreFoundation objects
# (only if not building the docs)
if not getattr(sys, 'skype4py_setup', False):
    carbon = Carbon()
    core = CoreFoundation()


class SkypeAPI(SkypeAPIBase):
    '''
    :note: Code based on Pidgin Skype Plugin source
           (http://code.google.com/p/skype4pidgin/).
           Permission was granted by the author.
    '''

    def __init__(self, opts):
        self.logger = logging.getLogger('Skype4Py.api.darwin.SkypeAPI')
        SkypeAPIBase.__init__(self)
        finalize_opts(opts)
        self.center = CFDistributedNotificationCenter()
        self.is_available = False
        self.client_id = -1

    def run(self):
        self.logger.info('thread started')
        self.loop = carbon.GetCurrentEventLoop()
        carbon.RunCurrentEventLoop()
        self.logger.info('thread finished')

    def close(self):
        if hasattr(self, 'loop'):
            self.loop.quit()
            self.client_id = -1
        SkypeAPIBase.close(self)

    def set_friendly_name(self, friendly_name):
        SkypeAPIBase.set_friendly_name(self, friendly_name)
        if self.attachment_status == apiAttachSuccess:
            # reattach with the new name
            self.set_attachment_status(apiAttachUnknown)
            self.attach()

    def attach(self, timeout, wait=True):
        if self.attachment_status in (apiAttachPendingAuthorization, apiAttachSuccess):
            return
        self.acquire()
        try:
            try:
                self.start()
            except AssertionError:
                pass
            t = threading.Timer(timeout2float(timeout), lambda: setattr(self, 'wait', False))
            try:
                self.init_observer()
                self.client_id = -1
                self.set_attachment_status(apiAttachPendingAuthorization)
                self.post('SKSkypeAPIAttachRequest')
                self.wait = True
                if wait:
                    t.start()
                while self.wait and self.attachment_status == apiAttachPendingAuthorization:
                    time.sleep(1.0)
            finally:
                t.cancel()
            if not self.wait:
                self.set_attachment_status(apiAttachUnknown)
                raise SkypeAPIError('Skype attach timeout')
            self.send_command(Command('PROTOCOL %s' % self.protocol))
        finally:
            self.release()

    def is_running(self):
        try:
            self.start()
        except AssertionError:
            pass
        self.init_observer()
        self.is_available = False
        self.post('SKSkypeAPIAvailabilityRequest')
        time.sleep(1.0)
        return self.is_available

    def startup(self, minimized, nosplash):
        if not self.is_running():
            from subprocess import Popen
            nul = file('/dev/null')
            Popen(['/Applications/Skype.app/Contents/MacOS/Skype'], stdin=nul, stdout=nul, stderr=nul)

    def send_command(self, command):
        if not self.attachment_status == apiAttachSuccess:
            self.attach(command.Timeout)
        self.push_command(command)
        self.notifier.sending_command(command)
        cmd = u'#%d %s' % (command.Id, command.Command)
        if command.Blocking:
            command._event = event = threading.Event()
        else:
            command._timer = timer = threading.Timer(command.timeout2float(), self.pop_command, (command.Id,))

        self.logger.debug('sending %s', repr(cmd))
        userInfo = CFDictionary({core.CFSTR('SKYPE_API_COMMAND'): CFString(cmd),
                                 core.CFSTR('SKYPE_API_CLIENT_ID'): CFNumber(self.client_id)})
        self.post('SKSkypeAPICommand', userInfo)

        if command.Blocking:
            event.wait(command.timeout2float())
            if not event.isSet():
                raise SkypeAPIError('Skype command timeout')
        else:
            timer.start()

    def init_observer(self):
        if self.has_observer():
            self.delete_observer()
        self.observer = CFString(self.friendly_name)
        self.center.add_observer(self.observer, self.SKSkypeAPINotification, 'SKSkypeAPINotification', immediate=True)
        self.center.add_observer(self.observer, self.SKSkypeWillQuit, 'SKSkypeWillQuit', immediate=True)
        self.center.add_observer(self.observer, self.SKSkypeBecameAvailable, 'SKSkypeBecameAvailable', immediate=True)
        self.center.add_observer(self.observer, self.SKAvailabilityUpdate, 'SKAvailabilityUpdate', immediate=True)
        self.center.add_observer(self.observer, self.SKSkypeAttachResponse, 'SKSkypeAttachResponse', immediate=True)

    def delete_observer(self):
        if not self.has_observer():
            return
        self.center.remove_observer(self.observer, 'SKSkypeAPINotification')
        self.center.remove_observer(self.observer, 'SKSkypeWillQuit')
        self.center.remove_observer(self.observer, 'SKSkypeBecameAvailable')
        self.center.remove_observer(self.observer, 'SKAvailabilityUpdate')
        self.center.remove_observer(self.observer, 'SKSkypeAttachResponse')
        del self.observer

    def has_observer(self):
        return hasattr(self, 'observer')

    def post(self, name, userInfo=None):
        if not self.has_observer():
            self.init_observer()
        self.center.post_notification(name, self.observer, userInfo, immediate=True)

    def SKSkypeAPINotification(self, center, observer, name, obj, userInfo):
        client_id = int(CFNumber(userInfo[core.CFSTR('SKYPE_API_CLIENT_ID')]))
        if client_id != 999 and (client_id == 0 or client_id != self.client_id):
            return
        cmd = unicode(CFString(userInfo[core.CFSTR('SKYPE_API_NOTIFICATION_STRING')]))
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

    def SKSkypeWillQuit(self, center, observer, name, obj, userInfo):
        self.logger.debug('received SKSkypeWillQuit')
        self.set_attachment_status(apiAttachNotAvailable)

    def SKSkypeBecameAvailable(self, center, observer, name, obj, userInfo):
        self.logger.debug('received SKSkypeBecameAvailable')
        self.set_attachment_status(apiAttachAvailable)

    def SKAvailabilityUpdate(self, center, observer, name, obj, userInfo):
        self.logger.debug('received SKAvailabilityUpdate')
        self.is_available = not not int(CFNumber(userInfo[core.CFSTR('SKYPE_API_AVAILABILITY')]))

    def SKSkypeAttachResponse(self, center, observer, name, obj, userInfo):
        self.logger.debug('received SKSkypeAttachResponse')
        # It seems that this notification is not called if the access is refused. Therefore we can't
        # distinguish between attach timeout and access refuse.
        if unicode(CFString(userInfo[core.CFSTR('SKYPE_API_CLIENT_NAME')])) == self.friendly_name:
            response = int(CFNumber(userInfo[core.CFSTR('SKYPE_API_ATTACH_RESPONSE')]))
            if response and self.client_id == -1:
                self.client_id = response
                self.set_attachment_status(apiAttachSuccess)
