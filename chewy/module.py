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
    '''Class to represent a Chewy module'''

    class PiecewiseConstruct(object):

        def __init__(self, repobase, path, version, description, *addons):
            self.addons = addons
            self.description = description
            self.path = path
            self.repobase = repobase
            self.version = version


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
            if kvp[0] == meta.ADDONS:
                self.addons.append(kvp[1])

            if kvp[0] == meta.PATH:
                if self.path is None:
                    self.path = kvp[1]
                else:
                    raise ModuleError('Multiple {} meta'.format(meta.PATH))

            if kvp[0] == meta.VERSION:
                if self.version is None:
                    self.version = kvp[1]
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

        if self.path is None:
            raise ModuleError('Path is not defined for module')
        if self.version is None:
            raise ModuleError('Version is not defined for module')
        if self.description is None:
            raise ModuleError('Description is not defined for module')
        if self.repobase is None:
            raise ModuleError('RepoBase is not defined for module')
