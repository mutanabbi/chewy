#!/usr/bin/env python
#
# Install script for `chewy`
#

import distutils.core
import portage.output
import sys

# this affects the names of all the directories we do stuff with
sys.path.insert(0, './')
import chewy

distutils.core.setup(
    name             = 'chewy'
  , version          = chewy.VERSION
  , description      = 'Python script to manage CMake modules'
  , maintainer       = 'Alex Turbov'
  , maintainer_email = 'I.zaufi@gmail.com'
  , url              = 'https://github.com/mutanabbi/chewy'
  , packages         = ['chewy']
  , scripts          = ['bin/chewy', 'bin/chewy-update-manifest']
    # TODO Is there any better way to determine a $dataroot_dir??
  , data_files       = [('share/doc/chewy-{}'.format(chewy.VERSION), ['AUTHORS', 'README.md'])]
  , license          = 'GPL-3'
  , classifiers      = [
        'Development Status :: 4 - Beta'
      , 'Environment :: Console'
      , 'Intended Audience :: Developers'
      , 'Intended Audience :: System Administrators'
      , 'License :: OSI Approved :: GNU General Public License (GPL-3)'
      , 'Natural Language :: English'
        # TODO Is it really Linux only?
      , 'Operating System :: POSIX :: Linux'
      , 'Programming Language :: Python'
        # TODO What about other Python versions?
      , 'Programming Language :: Python :: 3'
      , 'Topic :: Software Development'
      ]
  )
