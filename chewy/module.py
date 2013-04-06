#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Chewy Module class
#

import chewy.meta


_PATH_META = 'Path'
_VERSION_META = 'Version'
_DESCRIPTION_META = 'Description'
_ADDONS_META = 'Addons'
_REPOBASE_META = 'RepoBase'


class NoMetaError(RuntimeError):
    pass

class ModuleError(RuntimeError):
    pass


class Module(object):
    '''Class to represent a Chewy module'''

    def __init__(self, content):
        kvp_list = chewy.meta.parse(content)
        if not kvp_list:
            raise NoMetaError('No meta info found')

        # Default init members
        self.addons = []
        self.description = None
        self.path = None
        self.repobase = None
        self.version = None

        # Validate meta info
        for kvp in kvp_list:
            if kvp[0] == _ADDONS_META:
                self.addons.append(kvp[1])

            if kvp[0] == _PATH_META:
                if self.path is None:
                    self.path = kvp[1]
                else:
                    raise ModuleError('Multiple {} meta'.format(_PATH_META))

            if kvp[0] == _VERSION_META:
                if self.version is None:
                    self.version = kvp[1]
                else:
                    raise ModuleError('Multiple {} meta'.format(_VERSION_META))

            if kvp[0] == _DESCRIPTION_META:
                if self.description is None:
                    self.description = kvp[1]
                else:
                    raise ModuleError('Multiple {} meta'.format(_DESCRIPTION_META))

            if kvp[0] == _REPOBASE_META:
                if self.repobase is None:
                    self.repobase = kvp[1]
                else:
                    raise ModuleError('Multiple {} meta'.format(_REPOBASE_META))
