'''
Low level Skype for Linux interface implemented
using XWindows messaging. Uses direct Xlib calls
through ctypes module.

Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from Skype4Py.errors import ISkypeAPIError


def ISkypeAPI(handler, **opts):
    trans = opts.get('Transport', 'x11')
    if trans == 'dbus':
        from posix_dbus import ISkypeAPI
    elif trans == 'x11':
        from posix_x11 import ISkypeAPI
    else:
        raise ISkypeAPIError('Unknown transport: %s' % trans)
    return ISkypeAPI(handler, **opts)
