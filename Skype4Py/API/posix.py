'''
Low level Skype for Linux interface.

This module handles the options that you can pass to L{ISkype.__init__} for Linux machines.
The options include:

@newfield option: Option, Options

@option: C{Transport} (str) - Transport to use, either 'dbus' or 'x11'. If not specified, 'x11' is used.
Based on this option, the control is passed to either L{Skype4Py.API.posix_dbus} or L{Skype4Py.API.posix_x11}
submodules which may specify further options.
'''

from Skype4Py.errors import ISkypeAPIError


def _ISkypeAPI(handler, **opts):
    trans = opts.get('Transport', 'x11')
    if trans == 'dbus':
        from posix_dbus import _ISkypeAPI
    elif trans == 'x11':
        from posix_x11 import _ISkypeAPI
    else:
        raise ISkypeAPIError('Unknown transport: %s' % trans)
    return _ISkypeAPI(handler, **opts)
