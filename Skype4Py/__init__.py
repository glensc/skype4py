#
# Skype4Py
#

'''
Multiplatform Python wrapper for Skype.

  1. Usage.

     C{Skype4Py} is the package that you should import in your scripts to be able to access Skype.
     You won't need to import any submodules. Everything you may need will be available at the
     package level. This includes:

       - Classes
         - C{Skype4Py.Skype = L{Skype4Py.skype.ISkype}}
         - C{Skype4Py.CallChannelManager = L{Skype4Py.callchannel.ICallChannelManager}}
       - Constants
         - C{Skype4Py.* = L{Skype4Py.enums}.*}
       - Errors
         - C{Skype4Py.SkypeError = L{Skype4Py.errors.ISkypeError}}
         - C{Skype4Py.SkypeAPIError = L{Skype4Py.errors.ISkypeAPIError}}

     The first two are the only classes that you will be instatinating directly. Calling their methods/properties
     will give you the access to instances of all other classes, you won't have to instatinate them yourself.

     Every Skype4Py script instatinates the C{Skype4Py.Skype} class at least once. That's what you want to do
     first in your script. Then follow the L{Skype4Py.skype.ISkype} reference to see where you can get from
     there.

  2. Quick example.

     This short example connects to Skype client and prints the user's full name and the names of all the
     contacts from the contacts list::

         import Skype4Py

         skype = Skype4Py.Skype()

         # Connects Skype object to Skype client
         skype.Attach()

         print 'Your full name:', skype.CurrentUser.FullName
         print 'Your contacts:'
         for user in skype.Friends:
             print '    ', user.FullName

@author: U{Arkadiusz Wahlig<yak@nokix.pasjagsm.pl>}
@requires: Python 2.4 or newer
@see: U{The Skype4Py webpage<https://developer.skype.com/wiki/Skype4Py>}
@license: BSD License (see the accompanying LICENSE file for more information)
@copyright: S{copy} 2007 Arkadiusz Wahlig
'''

from skype import *
from callchannel import *
from enums import *
from errors import *


__version__ = '0.9.28.5'
'''The version of Skype4Py.'''

Skype = ISkype
CallChannelManager = ICallChannelManager

SkypeError = ISkypeError
SkypeAPIError = ISkypeAPIError
