"""
Low level *Skype for Linux* interface.

This module handles the options that you can pass to `Skype.__init__` for Linux machines.
The options include:

- ``Transport`` (str) - Name of a channel used to communicate with the Skype client.
  Currently supported values:
  
  - ``'x11'``

    Uses *X11* messaging through *Xlib*. This is the default if no transport is specified.

    Look into `api.posix_x11` module for additional options.

  - ``'dbus'``

    Uses *DBus* thrugh *dbus-python* package (must be installed separately).

    Look into `api.posix_dbus` for additional options.
"""
__docformat__ = 'restructuredtext en'


from Skype4Py.errors import SkypeAPIError


__all__ = ['SkypeAPI']


# the posix_x11 module has to be imported as soon as possible so it can initialize
# the X11 library; without this extra import it would be loaded during first Skype
# object instantiation; any possible exceptions are ignored because the module is
# not really needed at this point and the errors will be reported anyway during
# Skype object instantiation
try:
    import posix_x11
except:
    pass


def SkypeAPI(opts):
    trans = opts.pop('Transport', 'x11')
    if trans == 'dbus':
        from posix_dbus import SkypeAPI
    elif trans == 'x11':
        from posix_x11 import SkypeAPI
    else:
        raise SkypeAPIError('Unknown transport: %s' % trans)
    return SkypeAPI(opts)
