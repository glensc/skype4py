#!/usr/bin/env python

'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

from distutils.core import setup
from Skype4Py.skype import GetVersion
import os


LanguagesPath = 'Skype4Py/Languages'

setup(name='Skype4Py',
      version=str(GetVersion()),
      description='Skype API wrapper for Python.',
      long_description='Skype4Py is a high-level, platform independant Skype API\nwrapper for Python with API simmilar to Skype4COM.',
      author='Arkadiusz Wahlig',
      author_email='yak@nokix.pasjagsm.pl',
      url='http://skype4py.sourceforge.net',
      license='BSD License',
      platforms=['Windows 2000/XP', 'Linux'],
      packages=['Skype4Py', 'Skype4Py/API'],
      package_data={'Skype4Py': ['Languages/*']},
     )
