#!/usr/bin/env python
#
# Some tests for chewy
#

""" Unit tests for chewy.FancyGrid """

# Standard imports
import os
import sys
import unittest

sys.path.append('..')

# Project specific imports
import chewy

_test_case_1=[[1], [2], [3]]
_expect_1='''\
 1
 2
 3
'''
_test_case_2=[(1, 'uno'), (2, 'dos'), (3, 'tres')]
_expect_2='''\
1   uno
2   dos
3   tres
'''
_test_case_3=[(1, '-', 'uno'), (2, '-', 'dos'), (3, '-', 'tres')]
_expect_3='''\
1  -   uno
2  -   dos
3  -   tres
'''
_test_case_4=[(1, 'uno', '-'), (2, 'dos', '-'), (3, 'tres', '-')]
_expect_4='''\
1  uno    -
2  dos    -
3  tres   -
'''

class FancyGridTester(unittest.TestCase):
    '''Unit tests for chewy.FancyGrid'''

    def setUp(self):
        pass

    def test_one(self):
        result = str(chewy.FancyGrid(_test_case_1))
        self.assertEqual(result, _expect_1)

    def test_two(self):
        result = str(chewy.FancyGrid(_test_case_2))
        self.assertEqual(result, _expect_2)

    def test_three(self):
        result = str(chewy.FancyGrid(_test_case_3))
        self.assertEqual(result, _expect_3)

    def test_four(self):
        result = str(chewy.FancyGrid(_test_case_4))
        self.assertEqual(result, _expect_4)


if __name__ == '__main__':
    suite = unittest.makeSuite(FancyGridTester)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful() != True:
        sys.exit(1)

