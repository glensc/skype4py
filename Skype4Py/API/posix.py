'''
Low level Skype for Linux interface.

This module handles the options that you can pass to L{ISkype.__init__<skype.ISkype.__init__>} for Linux machines.
The options include:

@newfield option: Option, Options

@option: C{Transport} (str) - A transport is a channel used to communicate with Skype client. Currently supported values are:
  - C{'x11'}

  Uses X11 (libX) messaging. This is the default if no transport is specified.

  Look into L{Skype4Py.API.posix_x11} for additional options.

  - C{'dbus'}

  Uses DBus (python-dbus).

  Look into L{Skype4Py.API.posix_dbus} for additional options.
'''

from Skype4Py.errors import ISkypeAPIError


# the posix_x11 module has to be imported as soon as possible; without this extra
# import it would be loaded when Skype object is instantiated; any possible
# exceptions are ignored because the module is not really needed at this point;
# the errors will be reported during Skype object instantiation
try:
    import posix_x11
except:
    pass


def _ISkypeAPI(handler, opts):
    trans = opts.pop('Transport', 'x11')
    if trans == 'dbus':
        from posix_dbus import _ISkypeAPI
    elif trans == 'x11':
        from posix_x11 import _ISkypeAPI
    else:
        raise ISkypeAPIError('Unknown transport: %s' % trans)
    return _ISkypeAPI(handler, opts)
