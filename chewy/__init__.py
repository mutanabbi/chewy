#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Testable code for Chewy
#
#

from chewy.manifest import Manifest, ManifestError
from chewy.module import Module, ModuleError
from chewy.version import Version, VersionError
from chewy.session import Session
from chewy.session import HttpEndpoint
from chewy.fancy_grid import FancyGrid

class NoMetaError(RuntimeError):
    pass

import os
import fnmatch

EXPECTED_CMAKE_MODULES_PATH = 'cmake/modules'
VERSION="0.1"


def modules_dir_lookup(start_path = os.getcwd()):
    while start_path != '/':
        try_mod_dir = os.path.join(start_path, EXPECTED_CMAKE_MODULES_PATH)
        if os.path.isdir(try_mod_dir):
            # TODO: logging
            #log.einfo("Found CMake modules directory at `{}'".format(try_mod_dir))
            return try_mod_dir
        else:
            start_path = os.path.dirname(start_path)
    raise RuntimeError("Unable to find CMake modules directory `{}'".format(EXPECTED_CMAKE_MODULES_PATH))


def modules_lookup(modules_dir):
    ''' Return: list<string> or [] '''
    result = []
    for root, dirs, files in os.walk(modules_dir):
        result += [os.path.join(root, x) for x in fnmatch.filter(files, '*.cmake')]
    return result


class ModuleStatus(object):
    '''Class to represent a module status.'''

    UNKNOWN = -1
    SAME_SAME = 0                                           # ;-)
    DELETED = 1
    UPDATE_AVAILABLE = 2
    LOCALY_MODIFIED = 3

    __STATUS_STRINGS = {
        SAME_SAME: ' * '
      , DELETED: ' D '
      , UPDATE_AVAILABLE: ' U '
      , LOCALY_MODIFIED: ' M '
    }

    def __init__(self, mod):
        self.module = mod
        self.__status = ModuleStatus.UNKNOWN
        self.__available_version = None


    def set_remote_version(self, remote_version):
        self.__available_version = remote_version
        if remote_version is None:
            self.__status = ModuleStatus.DELETED
        elif self.module.version < remote_version:
            self.__status = ModuleStatus.UPDATE_AVAILABLE
        elif self.module.version > remote_version:
            self.__status = ModuleStatus.LOCALY_MODIFIED
        else:
            self.__status = ModuleStatus.SAME_SAME


    def available_version(self):
        return self.__available_version


    def status_as_string(self):
        if self.__status in self.__STATUS_STRINGS:
            return self.__STATUS_STRINGS[self.__status]
        return '???'


def collect_installed_modules(modules_dir):
    ''' Return: a dict of `repobase` to a list of `Module`, status, None '''

    # Group installed modules by unique repobase
    # dict<list<Modules>, status, remote_version>
    mod_list = {}
    for module_file in modules_lookup(modules_dir):
        try:
            with open(module_file, 'rt') as f:
                content = f.read()
                mod = Module(content)
                if not mod.repobase in mod_list:
                    mod_list[mod.repobase] = []
                mod_list[mod.repobase].append(ModuleStatus(mod))
        except NoMetaError:
            continue
        except ModuleError as e:
            # TODO: logging
            #log.ewarn('Module {} has error: {}'.format(module_file, e.args[0]))
            continue
    return mod_list


def find(seq, pred):
    return next(
        filter(lambda x: pred(x), seq)
      , None
      )
