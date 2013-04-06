#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Chewy Verstion class
#

import chewy
import chewy.meta as meta
import functools


class VersionError(RuntimeError):
    pass


@functools.total_ordering
class Version(object):

    def __init__(self, version):
        '''
            verstion: string by format MAJOR.MINOR (separated by .)
        '''
        try:
            self.major, self.minor = [int(i) for i in version.strip().split('.')]
        except ValueError as ex:
            raise VersionError from ex
        except AttributeError as ex:
            raise VersionError from ex

        if not (self.major and self.minor):
            raise VersionError('Incorrect version string: {}'.format(version))

        if self.major > 9999:
            raise VersionError('Major number too big: {}'.format(self.major))

        if self.minor > 9999:
            raise VersionError('Minor number too big: {}'.format(self.minor))


    def __lt__(self, other):
        return  self.major < other.major or (self.major == other.major and self.minor < other.minor)

    def __eq__(self, other):
        return (self.major, self.minor) == (other.major, other.minor)

    def __hash__(self):
        return self.major * 10000 + self.minor

