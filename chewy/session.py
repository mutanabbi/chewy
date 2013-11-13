#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import http.client
import os
import socket
import urllib.parse

import chewy


MANIFEST_PATH = 'manifest'
_HEADERS = {
    'User-Agent': 'Chewy 0.1'
  , 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
  , 'Accept-Language': 'en-us,en;q=0.7,ru;q=0.3'
  , 'DNT': 1
  , 'Connection': 'keep-alive'
  }


class NetworkError(RuntimeError):
    pass



class HttpEndpoint(urllib.parse.SplitResult):
    ''' Class to represent a HTTP endpoint to contact'''

    is_ssl = False

    def __new__(cls, url):
        return super(HttpEndpoint, cls).__new__(cls, *urllib.parse.urlsplit(url))

    def __init__(self, url):
        '''Parse the URL given and construct an endpoint instance'''
        self.url = url
        if self.scheme == 'http':
            self.is_ssl = False
        elif self.scheme == 'https':
            self.is_ssl = True
        else:
            raise RuntimeError("Unsupported scheme in URL `{}'".format(url))


class Factory(object):
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
            cs = Session(ep)
            self.__cp[key] = cs
            return cs



class Session(object):
    '''Class to access a remote CHEWY repository'''

    def __init__(self, endpoint):
        '''Connect the endpoint given and be ready for files transfer'''
        if not isinstance(endpoint, HttpEndpoint):
            raise TypeError('Endpoint to contact has invalid type')

        self.__ep = endpoint
        import socket
        try:
            if self.__ep.is_ssl:
                self.__connection = http.client.HTTPSConnection(self.__ep.hostname, self.__ep.port)
            else:
                self.__connection = http.client.HTTPConnection(self.__ep.hostname, self.__ep.port)
            self.__connection.connect()
        except socket.error as ex:
            raise NetworkError("hostname: `{}'; port: `{}': {}".format(self.__ep.hostname, self.__ep.port, ex))


    def close(self):
        self.__connection.close()


    def get_manifest(self):
        url = os.path.join(self.__ep.geturl(), MANIFEST_PATH)
        # TODO: logging
        #log.einfo("Trying to get `{}'".format(url))
        # TODO Translate and rethrow a possible exception?
        contents = self.retrieve_remote_file(url)
        manifest = chewy.Manifest(contents)
        assert('We expect the repobase is a part of URL' and manifest.repobase.startswith(self.__ep.geturl()))
        return manifest


    def retrieve_remote_file(self, file_path):
        '''Retrieve the file specified'''
        try:
            self.__connection.request('GET', file_path)
            r = self.__connection.getresponse()
        except socket.error as ex:
            raise NetworkError("hostname: `{}'; port: `{}': {}".format(self.__ep.hostname, self.__ep.port, ex))
        # request should be read any way if we want reuse this connection
        data = r.read()
        if r.status != http.client.OK:
            raise RuntimeError(
                "Unable to retrieve a file `{}': {} - {}".format(file_path, r.status, r.reason)
              )
        return data.decode('utf-8')


