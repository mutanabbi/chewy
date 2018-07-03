#!/usr/bin/env python
#
# Install script for `chewy`
#

# Standard imports
import pathlib
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import chewy

def sources_dir():
    return pathlib.Path(__file__).parent

def readfile(filename):
    with (sources_dir() / filename).open(encoding='UTF-8') as f:
        return f.read()

def get_requirements_from(filename):
    with (sources_dir() / filename).open(encoding='UTF-8') as f:
        return f.readlines()

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
      , 'Programming Language :: Python :: 3'
      , 'Topic :: Software Development :: Version Control'
      ]
  , install_requires = get_requirements_from('requirements.txt')
  , test_suite       = 'test'
  , zip_safe         = True
  )
