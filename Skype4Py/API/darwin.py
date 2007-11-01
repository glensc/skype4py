'''
Low level Skype for Mac OS interface.

Currently this is only a placeholder for future code.
'''

from Skype4Py.API import ICommand, _ISkypeAPIBase
import sys


if sys.argv != ['(imported)']:
    # if we're building docs, we don't want the exception to be raised
    raise OSError('MacOS is currently not supported by Skype4Py')
