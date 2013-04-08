#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Testable code for Chewy
#
#

from chewy.manifest import Manifest, ManifestError
from chewy.module import Module, ModuleError
from chewy.version import Version, VersionError

class NoMetaError(RuntimeError):
    pass

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



class HttpEndpoint(urllib.parse.SplitResult):
    ''' Class to represent a HTTP endpoint to contact'''

    is_ssl = False

    def __new__(cls, url):
        return super(HttpEndpoint, cls).__new__(cls, *urllib.parse.urlsplit(url))

    def __init__(self, url):
        '''Parse the URL given and construct an endpoint instance'''
        super(HttpEndpoint, self).__init__(urllib.parse.urlsplit(url))
        self.url = url
        if self.scheme == 'http':
            self.is_ssl = False
        elif self.scheme == 'https':
            self.is_ssl = True
        else:
            raise RuntimeError("Unsupported scheme in URL `{}'".format(url))



class SessionFactory(object):
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
            cs = ChewySession(ep)
            self.__cp[key] = cs
            return cs



class ChewySession(object):
    '''Class to access a remote CHEWY repository'''

    def __init__(self, endpoint):
        '''Connect the endpoint given and be ready for files transfer'''
        if not isinstance(endpoint, HttpEndpoint):
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
        return Manifest(contents)


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



class FancyGrid(object):
    # TODO: Move this code to some kind of unit test
    # t = [[55555.666, 'aaa', '20', 'aaaaaaaa', 66], [42.5, 'bbbbbbbbbbbbb', '44444', 'bb', 112], [42, 'cc', 3, 'ccc', 555555555555]]
    # print(FancyGrid(t))

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
        frmt = ('{{:<{}}}  ' * (cols - 1) + ' {{:<}}\n').format(*lens)

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


class ModuleStatus(object):
    '''Class to represent a module status.'''

    UNKNOWN = -1
    SAME_SAME = 0                                           # ;-)
    DELETED = 1
    UPDATE_AVAILABLE = 2
    LOCALY_MODIFIED = 3

    __STATUS_STRINGS = {
        SAME_SAME: ' * '
      , DELETED: ' D '
      , UPDATE_AVAILABLE: ' U '
      , LOCALY_MODIFIED: ' M '
    }

    def __init__(self, mod):
        self.module = mod
        self.__status = ModuleStatus.UNKNOWN
        self.__available_version = None


    def set_remote_version(self, remote_version):
        self.__available_version = remote_version
        if remote_version is None:
            self.__status = ModuleStatus.DELETED
        elif self.module.version < remote_version:
            self.__status = ModuleStatus.UPDATE_AVAILABLE
        elif self.module.version > remote_version:
            self.__status = ModuleStatus.LOCALY_MODIFIED
        else:
            self.__status = ModuleStatus.SAME_SAME


    def available_version(self):
        return self.__available_version


    def status_as_string(self):
        if self.__status in self.__STATUS_STRINGS:
            return self.__STATUS_STRINGS[self.__status]
        return '???'


def collect_installed_modules(modules_dir):
    ''' Return: a dict of `repobase` to a list of `Module`, status, None '''

    # Group installed modules by unique repobase
    # dict<list<Modules>, status, remote_version>
    mod_list = {}
    for module_file in modules_lookup(modules_dir):
        try:
            with open(module_file, 'rt') as f:
                content = f.read()
                mod = Module(content)
                if not mod.repobase in mod_list:
                    mod_list[mod.repobase] = []
                mod_list[mod.repobase].append(ModuleStatus(mod))
        except NoMetaError:
            continue
        except ModuleError as e:
            log.ewarn('Module {} has error: {}'.format(module_file, e.args[0]))
            continue
    return mod_list

