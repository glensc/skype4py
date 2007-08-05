'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from sys import builtin_module_names


class ICommand(object):
    def __init__(self, Id, Command, Expected=u'', Blocking=False, Timeout=30000):
        self.Id = Id
        self.Command = unicode(Command)
        self.Expected = unicode(Expected)
        self.Blocking = Blocking
        self.Timeout = Timeout
        self.Reply = u''


# Select apropriate low-level Skype API module
if 'posix' in builtin_module_names:
    from posix import *
elif 'nt' in builtin_module_names:
    from nt import *
else:
    raise OSError('OS not supported')
