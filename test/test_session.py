#!/usr/bin/env python
#
# Some tests for chewy.Session and chewy.Factory
#

""" Unit tests for chewy.Session """

# Standard imports
import http.client
import os
import sys
import unittest
from mock import patch

sys.path.insert(0, '..')

# Project specific imports
import chewy

_TEST_REPO_URL = 'http://localhost/chewy/repo'
_TEST_FILE_URL = 'http://localhost/chewy/repo/test.cmake'
_TEST_FILE_CONTENT = '''
# Sample
'''


class FakeHTTPResponse(object):
    def __init__(self):
        self.status = http.client.OK

    def read(self):
        class FakeData(object):
            def decode(self, encode):
                return _TEST_FILE_CONTENT
        return FakeData()


class FakeHTTPConnection(object):
    def __init__(self, suite):
        self.status = http.client.OK

    def connect(self):
        pass

    def close(self):
        pass

    def request(self, method, filename):
        pass

    def getresponse(self):
        return FakeHTTPResponse()



class ChewySessionTester(unittest.TestCase):
    '''Unit tests for [???]'''

    def setUp(self):
        self.connection = FakeHTTPConnection(self)


    @patch('http.client.HTTPConnection')
    def test_smth(self, mock_connection):
        # Configure mock HTTP connection
        mock_connection.return_value = self.connection

        # Get session for given repobase URL
        ep = chewy.HttpEndpoint(_TEST_REPO_URL)
        sf = chewy.session.Factory()
        session = sf.get_session(ep)
        contents = session.retrieve_remote_file(_TEST_FILE_URL)
        #mock_connection.request.assert_called_with('GET', _TEST_FILE_URL)
        return


if __name__ == '__main__':
    suite = unittest.makeSuite(ChewySessionTester)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
