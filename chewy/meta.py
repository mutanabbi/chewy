#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Chewy MetaInfo helpers
#

import re


_X_META_REGEX = re.compile(r'^\s*#\s+X-Chewy-([^:]+):\s*(.*)\s*$')

PATH = 'Path'
VERSION = 'Version'
DESCRIPTION = 'Description'
ADDON = 'AddonFile'
REPOBASE = 'RepoBase'


def parse(file_content):
    '''Try to parse given file content and get meta fields as list of KVP'''
    lines = file_content.split('\n')
    meta = []
    for line in lines:
        m = _X_META_REGEX.search(line)
        if m:
            meta.append((m.group(1).strip(), m.group(2).strip()))
    return meta

