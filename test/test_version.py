#!/usr/bin/env python
#
# Some tests for Chewy version
#

""" Unit tests for chewy.Version """

# Standard imports
import os
import sys
import unittest

sys.path.append('..')

# Project specific imports
import chewy


class ChewyVersionTester(unittest.TestCase):
    '''Unit tests for [???]'''

    def setUp(self):
        pass


    def test_version(self):
        ver1 = chewy.Version('1.2')
        ver2 = chewy.Version('1.3')
        self.assertTrue(ver1 < ver2)
        self.assertFalse(ver1 > ver2)
        self.assertFalse(ver1 == ver2)

        ver1 = chewy.Version('2.4')
        ver2 = chewy.Version('5.1')
        self.assertTrue(ver1 < ver2)
        self.assertFalse(ver1 > ver2)
        self.assertFalse(ver1 == ver2)

        ver1 = chewy.Version('05. 1')
        ver2 = chewy.Version('  20.4')
        self.assertTrue(ver1 < ver2)
        self.assertFalse(ver1 > ver2)
        self.assertFalse(ver1 == ver2)

    def test_exception(self):
        try:
            chewy.Version('5.h6')
            self.assertTrue(False)
        except chewy.VersionError:
            self.assertTrue(True)

        try:
            chewy.Version('')
            self.assertTrue(False)
        except chewy.VersionError:
            self.assertTrue(True)

        try:
            chewy.Version('56')
            self.assertTrue(False)
        except chewy.VersionError:
            self.assertTrue(True)

        try:
            chewy.Version(None)
            self.assertTrue(False)
        except chewy.VersionError:
            self.assertTrue(True)


if __name__ == '__main__':
    suite = unittest.makeSuite(ChewyVersionTester)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful() != True:
        sys.exit(1)
