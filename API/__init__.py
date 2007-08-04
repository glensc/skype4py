
from sys import builtin_module_names


class ICommand(object):
    def __init__(self, Id, Command, Expected='', Blocking=False, Timeout=30000):
        self.Id = Id
        self.Command = Command
        self.Expected = Expected
        self.Blocking = Blocking
        self.Timeout = Timeout
        self.Reply = ''


# Select apropriate low-level Skype API module
if 'posix' in builtin_module_names:
    from posix import *
elif 'nt' in builtin_module_names:
    from nt import *
else:
    raise OSError('OS not supported')
