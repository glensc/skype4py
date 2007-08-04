#!/usr/bin/env python

from distutils.core import setup

setup(name='Skype4Py',
      version='0.4.0.0',
      description='Skype API wrapper for Python.',
      long_description='Skype4Py is a high-level, platform independant Skype API\nwrapper for Python with API simmilar to Skype4COM.',
      author='Arkadiusz Wahlig',
      author_email='yak@nokix.pasjagsm.pl',
      url='http://sourceforge.net/projects/skype4py',
      license='BSD License',
      platforms=['Windows 2000/XP', 'Linux'],
      packages=['Skype4Py', 'Skype4Py/API'],
     )
