#!/usr/bin/env python
#
# Some tests for Chewy manifest
#

""" Unit tests for chewy.manifest """

# Standard imports
import os
import sys
import unittest

sys.path.append('..')

# Project specific imports
import chewy
import chewy.manifest

_test_case_1 = '''
# X-Chewy-RepoBase: https://raw.github.com/mutanabbi/chewy-cmake-rep/master/
test.cmake 2.0 description
'''
_invalid_case_1 = '''
# X-Chewy-RepoBase: https://raw.github.com/mutanabbi/chewy-cmake-rep/master/
'''


class ChewyModuleTester(unittest.TestCase):
    '''Unit tests for [???]'''

    def setUp(self):
        pass


    def test_empty_manifest(self):
        try:
            result = chewy.Manifest("")
            self.assertTrue(False)
        except chewy.NoMetaError:
            self.assertTrue(True)


    def test_manifest(self):
        manifest = chewy.Manifest(_test_case_1)
        self.assertEqual(manifest.repobase, 'https://raw.github.com/mutanabbi/chewy-cmake-rep/master/')
        self.assertEqual(len(manifest.modules), 1)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ChewyModuleTester)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful() != True:
        sys.exit(1)

