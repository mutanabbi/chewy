#!/usr/bin/env python
#
# Some tests for Chewy module
#

""" Unit tests for chewy.module """

# Standard imports
import os
import sys
import unittest

sys.path.append('..')

# Project specific imports
import chewy

_test_case_1 = '''
# X-Chewy-RepoBase: https://raw.github.com/mutanabbi/chewy-cmake-rep/master/
# X-Chewy-Path: AddBoostTests.cmake
# X-Chewy-Version: 2.0
# X-Chewy-Description: Integrate Boost unit tests into CMake infrastructure
'''


class ChewyModuleTester(unittest.TestCase):
    '''Unit tests for [???]'''

    def setUp(self):
        pass

    def test_empty_module(self):
        try:
            result = chewy.Module("")
            self.assertTrue(False)
        except chewy.NoMetaError:
            self.assertTrue(True)

    def test_module(self):
        mod = chewy.Module(_test_case_1)
        self.assertEqual(mod.repobase, 'https://raw.github.com/mutanabbi/chewy-cmake-rep/master/')
        self.assertEqual(mod.path, 'AddBoostTests.cmake')
        self.assertEqual(mod.version, '2.0')
        self.assertTrue(0 < len(mod.description))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ChewyModuleTester)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful() != True:
        sys.exit(1)

