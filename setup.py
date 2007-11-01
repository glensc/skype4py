#!/usr/bin/env python

'''
Copyright (c) 2007, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
'''

import sys, os
from distutils.core import setup
from distutils.cmd import Command
from Skype4Py import __version__


class DocCommand(Command):
    description = 'build the documentation'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            from epydoc import cli
            epydoc_config = os.path.join('doc', 'epydoc.conf')
            old_argv = sys.argv[1:]
            sys.argv[1:] = (
                '--config=%s' % epydoc_config,
                '--no-private', # epydoc bug, not read from config
                '--simple-term',
                '--verbose')
            cli.cli()
            sys.argv[1:] = old_argv

        except ImportError:
            print >>sys.stderr, 'epydoc not installed, skipping doc build.'


setup(name='Skype4Py',
      version=__version__,
      description='Skype API wrapper for Python.',
      long_description='Skype4Py is a high-level, platform independant Skype API\n' \
                       'wrapper for Python with API simmilar to Skype4COM.',
      author='Arkadiusz Wahlig',
      author_email='yak@nokix.pasjagsm.pl',
      maintainer='Arkadiusz Wahlig',
      url='http://skype4py.sourceforge.net',
      license='BSD License',
      platforms=('Windows 2000/XP', 'Linux'),
      packages=('Skype4Py', 'Skype4Py.API', 'Skype4Py.Languages'),
      provides=('Skype4Py',),
      cmdclass={'build_doc': DocCommand})
