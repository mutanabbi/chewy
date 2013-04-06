#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Chewy Manifest class
#

import chewy
import chewy.meta as meta


class ManifestError(RuntimeError):
    pass

class Manifest(object):
    '''Class to represent a Chewy module'''

    _MIN_RECORD_FIELDS = 3

    def __init__(self, file_content):
        kvp_list = meta.parse(file_content)
        if not kvp_list:
            raise chewy.NoMetaError('No meta info found')

        # Default init members
        self.repobase = None

        # Validate meta info
        for kvp in kvp_list:
            if kvp[0] == meta.REPOBASE:
                if self.repobase is None:
                    self.repobase = kvp[1]
                else:
                    raise ModuleError('Multiple {} meta'.format(meta.REPOBASE))

        # Read modules list line by line
        lines = file_content.split('\n')
        self.modules = []
        line_number = 0
        for l in lines:
            line_number += 1
            line = l.lstrip()
            # Check for commented line
            if not l or l.startswith('#'):
                continue                                    # Ignore comments
            # Split record into fields
            record = line.split()
            if len(record) < self._MIN_RECORD_FIELDS:       # Minumum fields: path, version, description
                raise ManifestError('Too few fields in record at line {}'.format(line_number))

            self.modules.append(chewy.Module(chewy.Module.PiecewiseConstruct(self.repobase, *record)))
