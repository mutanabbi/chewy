#!/usr/bin/env python
#
# Install script for `chewy`
#

import sys

from distutils.core import setup

# this affects the names of all the directories we do stuff with
sys.path.insert(0, './')

setup(
    name             = 'chewy'
  , version          = 0.1
  , description      = 'Python script to manage CMake modules'
  , maintainer       = 'Alex Turbov'
  , maintainer_email = 'I.zaufi@gmail.com'
  , url              = 'https://github.com/mutanabbi/chewy'
  , scripts          = ['chewy']
  , license          = 'GPL-3'
  , classifiers      = [
        'Development Status :: 4 - Beta'
      , 'Environment :: Console'
      , 'Intended Audience :: Developers'
      , 'Intended Audience :: System Administrators'
      , 'License :: OSI Approved :: GNU General Public License (GPL-3)'
      , 'Natural Language :: English'
      , 'Operating System :: POSIX :: Linux'
      , 'Programming Language :: Python'
      , 'Topic :: Software Development'
      ]
  )
