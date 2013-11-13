#!/usr/bin/env python
#
# Install script for `chewy`
#

import distutils.core
import sys

import chewy


def readfile(filename):
    with open(filename) as f:
        return f.read()


distutils.core.setup(
    name             = 'chewy'
  , version          = chewy.VERSION
  , description      = 'Python script to manage CMake modules'
  , long_description = readfile('README.md')
  , keywords         = 'CMake modules synchronizer'
  , maintainer       = 'Alex Turbov'
  , maintainer_email = 'I.zaufi@gmail.com'
  , url              = 'https://github.com/mutanabbi/chewy'
  , download_url     = 'https://github.com/mutanabbi/chewy/archive/version-{}.tar.gz'.format(chewy.VERSION)
  , packages         = ['chewy']
  , scripts          = ['bin/chewy', 'bin/chewy-update-manifest']
  , license          = 'GNU General Public License v3 or later (GPLv3+)'
  , classifiers      = [
        'Development Status :: 5 - Production/Stable'
      , 'Environment :: Console'
      , 'Intended Audience :: Developers'
      , 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
      , 'Natural Language :: English'
        # TODO Is it really Linux only?
      , 'Operating System :: POSIX :: Linux'
      , 'Programming Language :: Python'
        # TODO What about other Python versions?
      , 'Programming Language :: Python :: 3'
      , 'Topic :: Software Development :: Version Control'
      ]
  , install_requires = ['argparse', 'setuptools']
  )
