#!/usr/bin/env python
#
# Some tests for Chewy manifest
#

""" Unit tests for chewy.Manifest """

# Standard imports
import os
import sys
import unittest

sys.path.insert(0, '..')

# Project specific imports
import chewy
import chewy.manifest

_test_case_1 = '''
# X-Chewy-RepoBase: https://raw.github.com/mutanabbi/chewy-cmake-rep/master/
test.cmake 2.0 sample+description
'''
_test_case_2 = '''
# X-Chewy-RepoBase: https://raw.github.com/mutanabbi/chewy-cmake-rep/master/
test.cmake 2.0 sample+description some.file another.file
'''
_invalid_case_1 = '''
# X-Chewy-RepoBase: https://raw.github.com/mutanabbi/chewy-cmake-rep/master/
'''


class ChewyModuleTester(unittest.TestCase):
    '''Unit tests for chewy.Manifest'''

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
        self.assertEqual(manifest.modules[0].path, 'test.cmake')
        self.assertEqual(manifest.modules[0].version, chewy.Version('2.0'))
        self.assertEqual(manifest.modules[0].description, 'sample description')

    def test_manifest_with_addons(self):
        manifest = chewy.Manifest(_test_case_2)
        self.assertEqual(manifest.repobase, 'https://raw.github.com/mutanabbi/chewy-cmake-rep/master/')
        self.assertEqual(len(manifest.modules), 1)
        self.assertEqual(manifest.modules[0].path, 'test.cmake')
        self.assertEqual(manifest.modules[0].version, chewy.Version('2.0'))
        self.assertEqual(manifest.modules[0].description, 'sample description')
        self.assertEqual(len(manifest.modules[0].addons), 2)
        self.assertEqual(manifest.modules[0].addons[0], 'some.file')
        self.assertEqual(manifest.modules[0].addons[1], 'another.file')


if __name__ == '__main__':
    suite = unittest.makeSuite(ChewyModuleTester)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful() != True:
        sys.exit(1)

