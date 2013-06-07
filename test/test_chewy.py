#!/usr/bin/env python
#
# Some tests for chewy
#

""" Unit tests for Chewy """

# Standard imports
import os
import sys
import unittest

sys.path.insert(0, '..')

# Project specific imports
import chewy


class ChewyTester(unittest.TestCase):
    '''Unit tests for [???]'''

    def setUp(self):
        pass

    def test_smth(self):
        '''Add test code here'''
        pass

if __name__ == '__main__':
#    unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(ChewyTester)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful() != True:
        sys.exit(1)

