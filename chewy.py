#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#

import argparse
import portage.output
import http.client
import os
import sys
import urllib.parse

log = portage.output.EOutput()

_MANIFEST_PATH = 'manifest'
_EXPECTED_CMAKE_MODULES_PATH = 'cmake/modules'
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


class chewy_session:
    '''Class to access a remote CHEWY repository'''

    def __init__(self, endpoint):
        '''Connect the endpoint given and be ready for files transfer'''
        if not isinstance(endpoint, http_endpoint):
            raise TypeError('Endpoint to contact has invalid type')

        self.ep = endpoint
        if self.ep.is_ssl:
            self.connection = http.client.HTTPSConnection(self.ep.hostname, self.ep.port)
        else:
            self.connection = http.client.HTTPConnection(self.ep.hostname, self.ep.port)


    def get_manifest(self, url):
        log.einfo("Trying to get `{}'".format(url))
        # TODO Translate and rethrow a possible exception?
        contents = self.retrieve_remote_file(url)

        # Transform a list of strings into a tuple of (URI, version, description),
        # skipping commented lines
        return tuple(line.split() for line in contents.split('\n') if line.strip() and line[0] != '#')


    def retrieve_remote_file(self, file_path):
        '''Retrieve the file specified
        '''
        self.connection.request('GET', file_path)
        r = self.connection.getresponse()
        if r.status != http.client.OK:
            raise RuntimeError(
                "Unable to retrieve a file `{}': {} - {}".format(file_path, r.status, r.reason)
              )
        return r.read().decode('utf-8')



# TODO Do not close connection, it can be reused later to get a module
# TODO Use LRU cache (decorator) to obtain CHEWY session instance for particular repo
def rcv_list(rep_url):
    assert(rep_url)
    ep = http_endpoint(rep_url)
    cs = chewy_session(ep)
    return cs.get_manifest(os.path.join(ep.path, _MANIFEST_PATH))


def do_list(url_list):
    '''Execute `list' command'''
    if not url_list:
        log.eerror('At least one repository URL should be given')

    result = []
    repos = {}
    for url in url_list:
        repos[len(result)] = url
        result += rcv_list(url)

    # TODO: Ugly implemented fancy output :). Refactor it!
    # 0) remove repository name
    current_repo = None
    for i, module in enumerate(result):
        if i in repos:
            current_repo = repos[i]
        if module[0].index(current_repo) == 0:
            m = module[0].lstrip(current_repo)
        else:
            log.einfo("Manifest from the `{}' repository seem intact".format(current_repo))
            m = module[0]

        result[i] = (m, module[1], urllib.parse.unquote_plus(module[2]))
    # 1) get max size for 1st and 2nd columns
    lens = [0, 0]
    for i in result:
        lens[0] = max(lens[0], len(i[0]))
        lens[1] = max(lens[1], len(i[1]))
    frmt = '{{:{}}}  {{:{}}}  {{}}'.format(lens[0], lens[1])
    current_repo = None
    for i, module in enumerate(result):
        if i in repos:
            current_repo = repos[i]
            log.einfo("Modules from the `{}' repository".format(current_repo))

        print(frmt.format(module[0], module[1], module[2]))


# TODO Move HTTP connection code to reusable function/class
# TODO Use LRU cache (decorator) to obtain CHEWY session instance for particular repo
def rcv_file(file_url):
    assert(file_url)
    ep = http_endpoint(file_url)
    cs = chewy_session(ep)
    return cs.retrieve_remote_file(ep.path)


def do_get(url_list):
    if not url_list:
        log.eerror('At least one url should be passed')

    for url in url_list:
        # TODO Handle exceptions, do error reporting and try to continue
        data = rcv_file(url)                                # Get a remote file into string

        # Going to write just received data to the modules dir
        o = urllib.parse.urlsplit(url)
        os.makedirs(os.path.join(_modules_dir, os.path.dirname(o.path).strip('/')), exist_ok=True)
        f = open(os.path.join(_modules_dir, o.path.strip('/')), 'wt', encoding = 'utf-8')
        f.write(data.decode('utf-8'))
        # TODO Retrieve dependencies according manifest
        # TODO Version compare required as well


def modules_dir_lookup(start_path = os.getcwd()):
    while start_path != '/':
        try_mod_dir = os.path.join(start_path, _EXPECTED_CMAKE_MODULES_PATH)
        if os.path.isdir(try_mod_dir):
            log.einfo("Found CMake modules directory at `{}'".format(try_mod_dir))
            return try_mod_dir
        else:
            start_path = os.path.dirname(start_path)
    # TODO Throw instead and log later!?
    log.eerror("Unable to find CMake modules directory `{}'".format(_EXPECTED_CMAKE_MODULES_PATH))
    sys.exit(1)


def main():
    cmd_parser = argparse.ArgumentParser(description='Manage the project specific CMake modules')
    cmd_parser.add_argument(
        '-m'
      , '--modules-dir'
      , metavar = 'PATH'
      , help = 'CMake modules directory to operate with'
      )

    subparsers = cmd_parser.add_subparsers(help='Available sub-commands:', dest='cmd')

    list_parser = subparsers.add_parser(
        'list'
      , help='Repositories URI list. Empty list means to get a list of all'
        'repositories which are founded in installed files'
      )
    get_parser = subparsers.add_parser(
        'get'
      , help='Get file from repository and add it to the project as new one'
      )
    update_parser = subparsers.add_parser(
        'update'
      , help='Update [all] installed files from their repo-sources'
      )
    status_parser = subparsers.add_parser('status', help='Check status of [all] installed files')

    list_parser.add_argument('rep_url', metavar='REPO_URL', help='Repositories URI list', nargs='*')
    get_parser.add_argument('file_url', metavar='FILE_URL', help='Files URI list', nargs='+')
    update_parser.add_argument(
        'file_url'
      , metavar='FILE_URL'
      , help='Files URI list. Empty list means to update all installed files'
      , nargs='*'
      )
    status_parser.add_argument(
        'file_url'
      , metavar='FILE_URL'
      , help='Files URI list. Empty list means to check status of all installed files'
      , nargs='*'
      )

    args = cmd_parser.parse_args()

    if args.cmd == 'list':
        # To get a list of modules, the working directory is not required
        do_list(args.rep_url)
    else:
        # Initialize working directory
        global _modules_dir
        if args.work_dir:
            if os.path.isdir(args.work_dir):
                _modules_dir = args.work_dir
            else:
                log.eerror("Unable to find CMake modules directory `{}'".format(_EXPECTED_CMAKE_MODULES_PATH))
                sys.exit(1)
        else:
            _modules_dir = modules_dir_lookup()

        # Continue to dispatch a command...
        if args.cmd == 'get':
            do_get(args.file_url)


if __name__ == "__main__":
    main()
