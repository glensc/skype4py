'''
Low-level Skype API definitions.

This module imports one of the:

- `Skype4Py.api.darwin`
- `Skype4Py.api.posix`
- `Skype4Py.api.windows`

submodules based on the current platform.
'''
__docformat__ = 'restructuredtext en'


import sys
import threading

from Skype4Py.utils import *
from Skype4Py.enums import apiAttachUnknown
from Skype4Py.errors import SkypeAPIError


__all__ = ['Command', 'SkypeAPINotifier', 'SkypeAPIBase', 'timeout2float', 'SkypeAPI']


class Command(object):
    '''Represents an API command. Use `Skype.Command` to instantiate.

    To send a command to Skype, use `Skype.SendCommand`.
    '''

    def __init__(self, Command, Expected=u'', Blocking=False, Timeout=30000, Id=-1):
        '''Use `Skype.Command` to instantiate the object instead of doing it directly.
        '''

        self.Blocking = Blocking
        '''If set to True, `Skype.SendCommand` will block until the reply is received.
        
        :type: bool'''

        self.Command = tounicode(Command)
        '''Command string.
        
        :type: unicode'''

        self.Expected = tounicode(Expected)
        '''Expected reply.
        
        :type: unicode'''

        self.Id = Id
        '''Command Id.
        
        :type: int'''

        self.Reply = u''
        '''Reply after the command has been sent and Skype has replied.
        
        :type: unicode'''

        self.Timeout = Timeout
        '''Timeout if Blocking == True.
        
        :type: int'''

    def __repr__(self):
        return '<%s with Command=%s, Blocking=%s, Reply=%s, Id=%s>' % \
            (object.__repr__(self)[1:-1], repr(self.Command), self.Blocking, repr(self.Reply), self.Id)

    def timeout2float(self):
        '''A wrapper for `api.timeout2float` function. Returns the converted
        `Timeout` property.
        '''
        return timeout2float(self.Timeout)


class SkypeAPINotifier(object):
    def attachment_changed(self, status):
        pass

    def notification_received(self, notification):
        pass
        
    def sending_command(self, command):
        pass

    def reply_received(self, command):
        pass


class SkypeAPIBase(threading.Thread):
    def __init__(self, opts):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.debug_level = opts.pop('ApiDebugLevel', 0)
        self.friendly_name = u'Skype4Py'
        self.protocol = 5
        self.commands = {}
        self.commands_lock = threading.RLock()
        self.notifier = SkypeAPINotifier()
        self.attachment_status = apiAttachUnknown

    def _not_implemented(self):
        raise SkypeAPIError('Function not implemented')
        
    def finalize_opts(self, opts):
        if opts:
            raise TypeError('Unexpected option(s): %s' % ', '.join(opts.keys()))
        
    def set_notifier(self, notifier):
        self.notifier = notifier
        
    def push_command(self, command):
        self.commands_lock.acquire()
        if command.Id < 0:
            command.Id = 0
            while command.Id in self.commands:
                command.Id += 1
        if command.Id in self.commands:
            self.commands_lock.release()
            raise SkypeAPIError('Command Id conflict')
        self.commands[command.Id] = command
        self.commands_lock.release()

    def pop_command(self, id_):
        self.commands_lock.acquire()
        try:
            command = self.commands[id_]
            del self.commands[id_]
        except KeyError:
            command = None
        self.commands_lock.release()
        return command

    def close(self):
        pass

    def set_debug_level(self, level):
        self.debug_level = level

    def dprint(self, msg, *args, **kwargs):
        if self.debug_level >= kwargs.pop('level', 1):
            if args:
                msg = msg % args
            print >>sys.stderr, 'Skype4Py/API %s' % msg
        if kwargs:
            raise TypeError('unexpected additional keyword arguments')

    def set_friendly_name(self, friendly_name):
        self.friendly_name = friendly_name

    def set_attachment_status(self, attachment_status):
        if attachment_status != self.attachment_status:
            self.dprint('new attachment status: %s', attachment_status)
            self.attachment_status = attachment_status
            self.notifier.attachment_changed(attachment_status)

    def attach(self, timeout, wait=True):
        self._not_implemented()

    def is_running(self):
        self._not_implemented()

    def startup(self, minimized, nosplash):
        self._not_implemented()

    def shutdown(self):
        self._not_implemented()

    def send_command(self, Command):
        self._not_implemented()

    def security_context_enabled(self, context):
        self._not_implemented()

    def enable_security_context(self, context):
        self._not_implemented()


def timeout2float(timeout):
    '''Converts a timeout expressed in milliseconds or seconds into a timeout expressed
    in seconds using a floating point number.
    
    :Parameters:
      timeout : int, long or float
        The input timeout. Assumed to be expressed in number of
        milliseconds if the type is int or long. For float, assumed
        to be a number of seconds (or fractions thereof).
    
    :return: The timeout expressed in number of seconds (or fractions thereof).
    :rtype: float
    '''
    if isinstance(timeout, float):
        return timeout
    return timeout / 1000.0


# Select appropriate low-level Skype API module
if getattr(sys, 'skype4py_setup', False):
    # dummy
    SkypeAPI = lambda **Options: None
elif sys.platform.startswith('win'):
    from windows import SkypeAPI
elif sys.platform == 'darwin':
    from darwin import SkypeAPI
else:
    from posix import SkypeAPI


# Note. py2exe will include the darwin but not the posix module. This seems to be the case
# solely because of the "posix" name. It might be a bug in py2exe or modulefinder caused
# by a failed attempt to import a "posix" module by the os module. If this is encountered
# during modulefinder scanning, the Skype4Py.api.posix is simply ignored.
#
# That being said ideally we would like to exclude both of them but I couldn't find a way
# to cause py2exe to skip them. I think py2exe should expose mechanisms to cooperate with
# extension modules aware of its existence.
