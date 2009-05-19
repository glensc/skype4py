#
# Skype4Py
#

'''
Skype4Py is a multiplatform Skype API wrapper for Python.

  1. B{Usage.}

     C{Skype4Py} is the package that you should import in your scripts to be able to access Skype.
     You won't need to import any submodules. Everything you may need will be available at the
     package level. This includes:

       - Classes
         - C{Skype4Py.Skype = L{Skype4Py.skype.Skype}}
         - C{Skype4Py.CallChannelManager = L{Skype4Py.callchannel.CallChannelManager}}
       - Constants
         - C{Skype4Py.* = L{Skype4Py.enums}.*}
       - Errors
         - C{Skype4Py.SkypeError = L{Skype4Py.errors.SkypeError}}
         - C{Skype4Py.SkypeAPIError = L{Skype4Py.errors.SkypeAPIError}}
       - Functions
         - C{Skype4Py.use_generators = L{Skype4Py.utils.use_generators}}

     The first two are the only classes that you will be instantiating directly. Calling their methods/properties
     will give you the access to instances of all other classes, you won't have to instantiate them yourself.
     The two classes are also the only ones that provide event handlers (for more information about events,
     see the L{EventHandlingBase} class which is a baseclass of the above two classes).

     Every Skype4Py script instatinates the C{Skype4Py.Skype} class at least once. That's what you want to do
     first in your script. Then follow the L{Skype4Py.skype.Skype} reference to see where you can get from
     there.

  2. B{Quick example.}

     This short example connects to Skype client and prints the user's full name and the names of all the
     contacts from the contacts list::

         import Skype4Py

         # Create Skype instance
         skype = Skype4Py.Skype()

         # Connect Skype object to Skype client
         skype.Attach()

         print 'Your full name:', skype.CurrentUser.FullName
         print 'Your contacts:'
         for user in skype.Friends:
             print '    ', user.FullName

  3. B{Note on the naming convention.}
  
     Skype4Py uses two different naming conventions. The first one applies to interfaces derived from
     U{Skype4COM<https://developer.skype.com/Docs/Skype4COM>}, a COM library which was an inspiration for
     Skype4Py. This convention uses the C{CapCase} scheme for class names, properties, methods and their
     arguments. The constants use the C{mixedCase} scheme.
     
     The second naming convention is more I{Pythonic} and is used by all other parts of the package
     including internal objects. It uses mostly the same C{CapCase} scheme for class names (including
     exception names) with a small difference in abbreviations. Where the first convention would use
     a C{SkypeApiError} name, the second one uses C{SkypeAPIError}. Other names including properties,
     methods, arguments, variables and module names use lowercase letters with underscores.

@author: Arkadiusz Wahlig <arkadiusz.wahlig@gmail.com>
@requires: Python 2.4 up until but not including 3.0
@see: U{The Skype4Py website<https://developer.skype.com/wiki/Skype4Py>}
@license: BSD License (see the accompanying LICENSE file for more information)
@copyright: S{copy} 2007-2009 Arkadiusz Wahlig
'''

from skype import Skype
from callchannel import CallChannelManager
from errors import SkypeError, SkypeAPIError
from enums import *
from utils import use_generators


__version__ = '1.0.31.2'
'''The version of Skype4Py.'''

