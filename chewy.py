#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
#from os import walk


def rcv_list(rep_url):
    pass


def do_list(url_list):
    pass


def work_dir_lookup():
    SUFFIX = '/cmake/modules'
    cur_path = os.getcwd()
    while not cur_path == '/':
        if os.path.exists(cur_path + SUFFIX) and os.path.isdir(cur_path + SUFFIX):
            return cur_path
        else:
            cur_path = os.path.split(cur_path)[0]
    raise 'OOPS'



def main():
    cmd_parser = argparse.ArgumentParser(description='Manage the project specific CMake modules')
    cmd_parser.add_argument('-w', '--work-dir', metavar = 'PATH', help = "Work directory (CMake modules storage)")

    subparsers = cmd_parser.add_subparsers(help="Available sub-commands:", dest = 'cmd')

    list_parser = subparsers.add_parser('list', help = "Repositories' URI list. Empty list means to get a list of all repositories' which are founded in installed files")
    get_parser = subparsers.add_parser('get', help = "Get file from repository and add it to the project as new one")
    update_parser = subparsers.add_parser('update', help = "Update [all] installed files from their repo-sources")
    status_parser = subparsers.add_parser('status', help = "Check status of [all] installed files")

    list_parser.add_argument('rep_uri', metavar = 'REP_URI', help = "Repositories' URI list", nargs = '*' )
    get_parser.add_argument('file_uri', metavar = 'FILE_URI', help = "Files' URI list", nargs = '+' )
    update_parser.add_argument('file_uri', metavar = 'FILE_URI', help = "Files' URI list. Empty list means to update all installed files", nargs = '*' )
    status_parser.add_argument('file_uri', metavar = 'FILE_URI', help = "Files' URI list. Empty list means to check status of all installed files", nargs = '*' )

    args = cmd_parser.parse_args()

    # DEBUG ONLY
    print(dir(args))
    print(args.cmd)
    print(args.file_uri)

    work_dir = args.work_dir if args.work_dir else work_dir_lookup()
    print('Workdir: {}'.format(work_dir))

    #for root, dirs, files in walk('../', topdown = False):
    #    print('-----------------------')
    #    print(root, files)

if __name__ == "__main__":
    main()
