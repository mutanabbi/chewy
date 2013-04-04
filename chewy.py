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

_MANIFEST_PATH = '/manifest'
_EXPECTED_CMAKE_MODULES_PATH = '/cmake/modules'

def rcv_list(rep_url):
    assert(rep_url)
    o = urllib.parse.urlsplit(rep_url)
    if o.scheme == 'http':
        conn = http.client.HTTPConnection(o.hostname, o.port)
    elif o.scheme == 'https':
        conn = http.client.HTTPSConnection(o.hostname, o.port)
    else:
        raise RuntimeError('Unsupported URL scheme')

    # TODO Use os.path.join() ???
    conn.request('GET', o.path + _MANIFEST_PATH)
    r = conn.getresponse()
    if not r.status == http.client.OK:
        raise RuntimeError('Unable to get manifest: %{} - %{}' % r.status, r.reason)
    data = r.read()                                         # Read the body of the response

    # Transform a list of strings into a tuple of (URI, version, description),
    # skipping commented lines
    return tuple(line.split() for line in data.decode('utf-8').split('\n') if line.strip() and line[0] != '#')


def do_list(url_list):
    result = []
    for url in url_list:
        result += rcv_list(url)

    # TODO: Ugly implemented fancy output :). Refactor it!
    lens = [0, 0]
    for i in result:
        lens[0] = max(lens[0], len(i[0]))
        lens[1] = max(lens[1], len(i[1]))
    frmt = '{{:{}}}\t{{:{}}}\t{{}}'.format(lens[0], lens[1])
    for i in result:
        print(frmt.format(i[0], i[1], urllib.parse.unquote_plus(i[2])))


def rcv_file(file_url):
    assert(file_url)
    o = urllib.parse.urlsplit(file_url)
    if o.scheme == 'http':
        conn = http.client.HTTPConnection(o.hostname, o.port)
    elif o.scheme == 'https':
        conn = http.client.HTTPSConnection(o.hostname, o.port)
    else:
        raise RuntimeError('Unsupported scheme')
    conn.request('GET', o.path)
    # TODO: get manifest to check dependencies
    r = conn.getresponse()
    if not r.status == http.client.OK:
        raise RuntimeError('Unable to get manifest: %{} - %{}' % r.status, r.reason)
    return r.read()



def do_get(url_list):
    assert("At least one url should be passed" and url_list)
    for url in url_list:
        o = urllib.parse.urlsplit(url)
        data = rcv_file(url)
        os.makedirs(os.path.join(_work_dir, os.path.dirname(o.path).strip('/')), exist_ok = True)
        f = open(os.path.join(_work_dir, o.path.strip('/')), 'wt', encoding = 'utf-8')
        f.write(data.decode('utf-8'))


def work_dir_lookup():
    cur_path = os.getcwd()
    while cur_path != '/':
        if os.path.isdir(cur_path + EXPECTED_CMAKE_MODULES_PATH):
            return cur_path
        else:
            cur_path = os.path.split(cur_path)[0]
    raise RuntimeError('OOPS')


def main():
    cmd_parser = argparse.ArgumentParser(description='Manage the project specific CMake modules')
    cmd_parser.add_argument(
        '-w'
      , '--work-dir'
      , metavar = 'PATH'
      , help = 'Work directory (CMake modules storage)'
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

    list_parser.add_argument('rep_uri', metavar='REP_URI', help='Repositories URI list', nargs='*')
    get_parser.add_argument('file_uri', metavar='FILE_URI', help='Files URI list', nargs='+')
    update_parser.add_argument(
        'file_uri'
      , metavar='FILE_URI'
      , help='Files URI list. Empty list means to update all installed files'
      , nargs='*'
      )
    status_parser.add_argument(
        'file_uri'
      , metavar='FILE_URI'
      , help='Files URI list. Empty list means to check status of all installed files'
      , nargs='*'
      )

    args = cmd_parser.parse_args()

    if args.cmd == 'list':
        # To get a list of modules, the working directory is not required
        do_list(args.rep_uri)
    else
        # Initialize working directory
        global _work_dir
        if args.work_dir:
            if os.path.isdir(args.work_dir):
                _work_dir = args.work_dir
            else:
                raise RuntimeError('You point to a wrong working directory')
        else:
            _work_dir = work_dir_lookup()

        # Continue to dispatch a command...
        if args.cmd == 'get':
            do_get(args.file_uri)

    #for root, dirs, files in walk('../', topdown = False):
    #    print('-----------------------')
    #    print(root, files)

if __name__ == "__main__":
    main()
