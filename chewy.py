#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse


def parse_list():
    pass

def parse_get():
    pass

def parse_update():
    pass

def parse_status():
    pass


def main():
    cmd_parser = argparse.ArgumentParser(description='Manage the project specific CMake modules')

    subparsers = cmd_parser.add_subparsers(help="Available sub-commands:")

    list_parser = subparsers.add_parser('list', help = "Repositories' URI list. Empty list means to get a list of all repositories' which are founded in installed files")
    get_parser = subparsers.add_parser('get', help = "Get file from repository and add it to the project as new one")
    update_parser = subparsers.add_parser('update', help = "Update [all] installed files from their repo-sources")
    status_parser = subparsers.add_parser('status', help = "Check status of [all] installed files")

    list_parser.add_argument('rep_uri', metavar = 'REP_URI', help = "Repositories' URI list", nargs = '*' )
    get_parser.add_argument('file_uri', metavar = 'FILE_URI', help = "Files' URI list", nargs = '+' )
    update_parser.add_argument('file_uri', metavar = 'FILE_URI', help = "Files' URI list. Empty list means to update all installed files", nargs = '*' )
    status_parser.add_argument('file_uri', metavar = 'FILE_URI', help = "Files' URI list. Empty list means to check status of all installed files", nargs = '*' )

    cmd_parser.parse_args()

if __name__ == "__main__":
    main()
