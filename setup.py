#!/usr/bin/env python
#
# Install script for `chewy`
#

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import chewy


def readfile(filename):
    with open(filename, encoding='UTF-8') as f:
        return f.read()


setup(
    name             = 'chewy'
  , version          = chewy.__version__
  , description      = 'Python script to manage CMake modules'
  , long_description = readfile('README.md')
  , keywords         = 'CMake modules synchronizer'
  , maintainer       = 'Alex Turbov'
  , maintainer_email = 'I.zaufi@gmail.com'
  , url              = 'https://github.com/mutanabbi/chewy'
  , download_url     = 'https://github.com/mutanabbi/chewy/archive/version-{}.tar.gz'.format(chewy.__version__)
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
      , 'Programming Language :: Python :: 3.4'
      , 'Topic :: Software Development :: Version Control'
      ]
  , install_requires = ['setuptools']
  , test_suite       = 'test'
  )
