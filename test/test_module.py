#!/usr/bin/env python
#
# Some tests for Chewy module
#

""" Unit tests for chewy.Module """

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
_invalid_case_1 = '''
# X-Chewy-RepoBase: https://raw.github.com/mutanabbi/chewy-cmake-rep/master/
'''
_invalid_case_2 = '''
# X-Chewy-RepoBase: https://raw.github.com/mutanabbi/chewy-cmake-rep/master/
# X-Chewy-Path: AddBoostTests.cmake
'''
_invalid_case_3 = '''
# X-Chewy-RepoBase: https://raw.github.com/mutanabbi/chewy-cmake-rep/master/
# X-Chewy-Path: AddBoostTests.cmake
# X-Chewy-Version: 2.0
'''


class ChewyModuleTester(unittest.TestCase):
    '''Unit tests for chewy.Module'''

    def setUp(self):
        pass


    def test_empty_module(self):
        try:
            result = chewy.Module("")
            self.assertTrue(False)
        except chewy.NoMetaError:
            self.assertTrue(True)


    def test_invalid_module_1(self):
        try:
            result = chewy.Module(_invalid_case_1)
            self.assertTrue(False)
        except chewy.ModuleError:
            self.assertTrue(True)


    def test_invalid_module_2(self):
        try:
            result = chewy.Module(_invalid_case_2)
            self.assertTrue(False)
        except chewy.ModuleError:
            self.assertTrue(True)


    def test_invalid_module_3(self):
        try:
            result = chewy.Module(_invalid_case_3)
            self.assertTrue(False)
        except chewy.ModuleError:
            self.assertTrue(True)


    def test_module(self):
        mod = chewy.Module(_test_case_1)
        self.assertEqual(mod.repobase, 'https://raw.github.com/mutanabbi/chewy-cmake-rep/master/')
        self.assertEqual(mod.path, 'AddBoostTests.cmake')
        self.assertEqual(mod.version, chewy.Version('2.0'))
        self.assertTrue(0 < len(mod.description))


    def test_module_alt(self):
        mod = chewy.Module(chewy.Module.PiecewiseConstruct('repobase', 'test.cmake', '1.0', 'description'))
        self.assertEqual(mod.repobase, 'repobase')
        self.assertEqual(mod.path, 'test.cmake')
        self.assertEqual(mod.version, chewy.Version('1.0'))
        self.assertEqual(mod.description, 'description')


class ChewyModuleStatusTester(unittest.TestCase):
    '''Unit tests for chewy.ModuleStatus'''

    def setUp(self):
        pass


    def test_module_status_1(self):
        mod = chewy.Module(_test_case_1)
        status = chewy.ModuleStatus(mod)
        status.set_remote_version(chewy.Version('1.0'))
        self.assertFalse(status.needs_update())


    def test_module_status_2(self):
        mod = chewy.Module(_test_case_1)
        status = chewy.ModuleStatus(mod)
        status.set_remote_version(chewy.Version('2.0'))
        self.assertFalse(status.needs_update())


    def test_module_status_3(self):
        mod = chewy.Module(_test_case_1)
        status = chewy.ModuleStatus(mod)
        status.set_remote_version(chewy.Version('2.1'))
        self.assertTrue(status.needs_update())


    def test_module_status_4(self):
        mod = chewy.Module(_test_case_1)
        status = chewy.ModuleStatus(mod)
        status.set_remote_version(chewy.Version('3.5'))
        self.assertTrue(status.needs_update())


if __name__ == '__main__':
    module_suite = unittest.TestLoader().loadTestsFromTestCase(ChewyModuleTester)
    status_suite = unittest.TestLoader().loadTestsFromTestCase(ChewyModuleStatusTester)
    module_result = unittest.TextTestRunner(verbosity=2).run(module_suite)
    status_result = unittest.TextTestRunner(verbosity=2).run(status_suite)
    if module_result.wasSuccessful() != True or status_result.wasSuccessful() != True:
        sys.exit(1)

