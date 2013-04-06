#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Testable code for Chewy
#
#

from chewy.module import Module, NoMetaError, ModuleError

import portage.output
import http.client
import os
import sys
import urllib.parse
import functools
import fnmatch

log = portage.output.EOutput()

MANIFEST_PATH = 'manifest'
EXPECTED_CMAKE_MODULES_PATH = 'cmake/modules'
VERSION="0.1"
_HEADERS = {
    'User-Agent': 'Chewy 0.1'
  , 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
  , 'Accept-Language': 'en-us,en;q=0.7,ru;q=0.3'
  , 'DNT': 1
  , 'Connection': 'keep-alive'
  }



class http_endpoint(urllib.parse.SplitResult):
    ''' Class to represent a HTTP endpoint to contact'''

    is_ssl = False

    def __new__(cls, url):
        return super(http_endpoint, cls).__new__(cls, *urllib.parse.urlsplit(url))

    def __init__(self, url):
        '''Parse the URL given and construct an endpoint instance'''
        super(http_endpoint, self).__init__(urllib.parse.urlsplit(url))
        self.url = url
        if self.scheme == 'http':
            self.is_ssl = False
        elif self.scheme == 'https':
            self.is_ssl = True
        else:
            raise RuntimeError("Unsupported scheme in URL `{}'".format(url))



class session_factory(object):
    def __init__(self):
        self.__cp = {}

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        for domain in self.__cp:
            self.__cp[domain].close()

    def get_session(self, ep):
        key = ep.scheme, ep.hostname, ep.port
        if key in self.__cp:
            return self.__cp[key]
        else:
            cs = chewy_session(ep)
            self.__cp[key] = cs
            return cs



class chewy_session(object):
    '''Class to access a remote CHEWY repository'''

    def __init__(self, endpoint):
        '''Connect the endpoint given and be ready for files transfer'''
        if not isinstance(endpoint, http_endpoint):
            raise TypeError('Endpoint to contact has invalid type')

        self.__ep = endpoint
        if self.__ep.is_ssl:
            self.__connection = http.client.HTTPSConnection(self.__ep.hostname, self.__ep.port)
        else:
            self.__connection = http.client.HTTPConnection(self.__ep.hostname, self.__ep.port)
        self.__connection.connect()


    def close(self):
        self.__connection.close()


    def get_manifest(self):
        url = os.path.join(self.__ep.geturl(), MANIFEST_PATH)
        log.einfo("Trying to get `{}'".format(url))
        # TODO Translate and rethrow a possible exception?
        contents = self.retrieve_remote_file(url)

        # Transform a list of strings into a tuple of (URI, version, description),
        # skipping commented lines
        return [line.split() for line in contents.split('\n') if line.strip() and line[0] != '#']


    def retrieve_remote_file(self, file_path):
        '''Retrieve the file specified'''
        self.__connection.request('GET', file_path)
        r = self.__connection.getresponse()
        # request should be read any way if we want reuse this connection
        data = r.read()
        if r.status != http.client.OK:
            raise RuntimeError(
                "Unable to retrieve a file `{}': {} - {}".format(file_path, r.status, r.reason)
              )
        return data.decode('utf-8')



class fancy_grid(object):
    # TODO: Move this code to some kind of unit test
    # t = [[55555.666, 'aaa', '20', 'aaaaaaaa', 66], [42.5, 'bbbbbbbbbbbbb', '44444', 'bb', 112], [42, 'cc', 3, 'ccc', 555555555555]]
    # print(fancy_grid(t))

    def __init__(self, table):
        ''' Pass any sequence of sequences here '''
        # TODO: Support generators (iterable objects of any type)
        assert(hasattr(table, '__iter__') and hasattr(table[0], '__iter__'))
        # TODO: assert all raws contains same number of fields

        rows = len(table)
        cols = len(table[0])

        ## 1) get max size for columns from 1st till last - 1
        lens = [0 for x in range(cols - 1)]
        for i in table:
            for n in range(cols - 1):
                lens[n] = max(len(str(i[n])), lens[n])
        frmt = ('{{:<{}}} ' * (cols - 1) + '{{:<}}\n').format(*lens)

        self.__s = ''
        for i in table:
            self.__s += frmt.format(*i)

    def __str__(self):
        return self.__s


def modules_dir_lookup(start_path = os.getcwd()):
    while start_path != '/':
        try_mod_dir = os.path.join(start_path, EXPECTED_CMAKE_MODULES_PATH)
        if os.path.isdir(try_mod_dir):
            log.einfo("Found CMake modules directory at `{}'".format(try_mod_dir))
            return try_mod_dir
        else:
            start_path = os.path.dirname(start_path)
    raise RuntimeError("Unable to find CMake modules directory `{}'".format(EXPECTED_CMAKE_MODULES_PATH))


def modules_lookup(modules_dir):
    ''' Return: list<string> or [] '''
    result = []
    for root, dirs, files in os.walk(modules_dir):
        result += [os.path.join(root, x) for x in fnmatch.filter(files, '*.cmake')]
    return result



