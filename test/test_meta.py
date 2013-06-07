#!/usr/bin/env python
#
# Some tests for Chewy meta
#

""" Unit tests for chewy.meta """

# Standard imports
import os
import sys
import unittest

sys.path.insert(0, '..')

# Project specific imports
import chewy.meta

_test_case_1 = '''
# X-Chewy-Test: sample    \n
'''

_test_case_2 = '''
# X-Chewy-Test: sample

some text

  #    X-Chewy-Test-2:    sample 2
'''

class ChewyMetaTester(unittest.TestCase):
    '''Unit tests for [???]'''

    def setUp(self):
        pass

    def test_empty_meta(self):
        result = chewy.meta.parse("")
        self.assertEqual(len(result), 0)

    def test_empty_meta_2(self):
        result = chewy.meta.parse("#\n#   \n   #")
        self.assertEqual(len(result), 0)

    def test_meta(self):
        result = chewy.meta.parse(_test_case_1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "Test")
        self.assertEqual(result[0][1], "sample")

    def test_meta_2(self):
        result = chewy.meta.parse(_test_case_2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "Test")
        self.assertEqual(result[0][1], "sample")
        self.assertEqual(result[1][0], "Test-2")
        self.assertEqual(result[1][1], "sample 2")


if __name__ == '__main__':
    suite = unittest.makeSuite(ChewyMetaTester)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful() != True:
        sys.exit(1)

