'''
Low level Skype for Mac OS X interface.

Currently this is only a placeholder for future code.
'''

from Skype4Py.API import ICommand, _ISkypeAPIBase
import sys


# if we're building docs, we don't want the exception to be raised;
# hence, the "if"
if sys.argv != ['(imported)']:
    raise OSError('Mac OS X is currently not supported by Skype4Py')
