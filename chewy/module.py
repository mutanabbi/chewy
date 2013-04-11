#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Chewy Module class
#

import chewy
import chewy.meta as meta


class ModuleError(RuntimeError):
    pass


class Module(object):
    '''
        Class to represent a Chewy module
        contain fields (getters):
            string repobase - repo URL and basedir
            string path     - relative to repobase file-path
            verstion        - string
            description     - string
            addons          - list<string>
    '''

    class PiecewiseConstruct(object):

        def __init__(self, repobase, path, version, description, *addons):
            self.addons = addons
            self.description = description
            self.path = path
            self.repobase = repobase
            self.version = chewy.Version(version)

    def __eq__ (self, other):
        '''
            Module is equal comparable, but note It isn't depended from module version
        '''
        return (self.repobase, self.path) == (other.repobase, other.path)


    def __init__(self, ctor_data):
        ''' Make a module from file content

            NOTE Unknown meta fileds are ignored
        '''
        # Default init members
        self.addons = []
        self.description = None
        self.path = None
        self.repobase = None
        self.version = None

        if isinstance(ctor_data, Module.PiecewiseConstruct):
            self.addons = ctor_data.addons
            self.description = ctor_data.description
            self.path = ctor_data.path
            self.repobase = ctor_data.repobase
            self.version = ctor_data.version
            return

        if not isinstance(ctor_data, str):
            raise TypeError('Module expect the only string parameter')

        kvp_list = meta.parse(ctor_data)
        if not kvp_list:
            raise chewy.NoMetaError('No meta info found')

        # Validate meta info
        for kvp in kvp_list:
            if kvp[0] == meta.ADDON:
                self.addons.append(kvp[1])

            if kvp[0] == meta.PATH:
                if self.path is None:
                    self.path = kvp[1]
                else:
                    raise ModuleError('Multiple {} meta'.format(meta.PATH))

            if kvp[0] == meta.VERSION:
                if self.version is None:
                    self.version = chewy.Version(kvp[1])
                else:
                    raise ModuleError('Multiple {} meta'.format(meta.VERSION))

            if kvp[0] == meta.DESCRIPTION:
                if self.description is None:
                    self.description = kvp[1]
                else:
                    raise ModuleError('Multiple {} meta'.format(meta.DESCRIPTION))

            if kvp[0] == meta.REPOBASE:
                if self.repobase is None:
                    self.repobase = kvp[1]
                else:
                    raise ModuleError('Multiple {} meta'.format(meta.REPOBASE))

        # Check that all attributes are here
        if self.path is None:
            raise ModuleError('Path is not defined for module')
        if self.version is None:
            raise ModuleError('Version is not defined for module')
        if self.description is None:
            raise ModuleError('Description is not defined for module')
        if self.repobase is None:
            raise ModuleError('RepoBase is not defined for module')


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


    def needs_update(self):
        return ModuleStatus.UPDATE_AVAILABLE == self.__status
