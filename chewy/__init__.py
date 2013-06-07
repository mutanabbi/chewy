#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Testable code for Chewy
#
#


from chewy.manifest import Manifest, ManifestError
from chewy.module import Module, ModuleStatus, ModuleError
from chewy.version import Version, VersionError
from chewy.session import Session
from chewy.session import HttpEndpoint
from chewy.fancy_grid import FancyGrid

import shutil
import os
import fnmatch

EXPECTED_CMAKE_MODULES_PATH = 'cmake/modules'
VERSION="0.1"


class NoMetaError(RuntimeError):
    pass


def modules_dir_lookup(start_path = os.getcwd()):
    while start_path != '/':
        try_mod_dir = os.path.join(start_path, EXPECTED_CMAKE_MODULES_PATH)
        if os.path.isdir(try_mod_dir):
            return try_mod_dir
        else:
            start_path = os.path.dirname(start_path)
    raise RuntimeError("Unable to find CMake modules directory `{}'".format(EXPECTED_CMAKE_MODULES_PATH))


def modules_lookup(modules_dir):
    ''' Return: list<string> or [] '''
    result = []
    # TODO: Check file is module by internal X-Chewy tags
    for root, dirs, files in os.walk(modules_dir):
        result += [os.path.join(root, x) for x in fnmatch.filter(files, '*.cmake')]
    return result


def open_module(module_file):
    with open(module_file, 'rt') as f:
        content = f.read()
        return Module(content)


def collect_installed_modules(modules_dir):
    ''' Return: a dict of `repobase` to a list of `Module`, status, None '''

    # Group installed modules by unique repobase
    # dict<list<Modules>, status, remote_version>
    mod_list = {}
    for module_file in modules_lookup(modules_dir):
        try:
            mod = open_module(module_file)
            if not mod.repobase in mod_list:
                mod_list[mod.repobase] = []
            mod_list[mod.repobase].append(ModuleStatus(mod))
        except (NoMetaError, ModuleError, IOError) as ex:
            # TODO: logging
            #log.ewarn('Module {} has error: {}'.format(module_file, ex))
            continue
    return mod_list


def find(seq, pred):
    return next(
        filter(lambda x: pred(x), seq)
      , None
      )


class PathError(RuntimeError):
    pass


# TODO: unittests
def sandbox_path(prefix, path):
    assert(
        'We expect prefix is an absolute path in the function by security reason'
        and prefix == os.path.abspath(prefix)
      )
    abspath = os.path.abspath(os.path.join(prefix, path))
    if not abspath.startswith(prefix):
        raise PathError(
            'Relative pathname {} trying to pass the sandbox {}'.format(path, abspath)
          )
    return abspath


# TODO: unittests
def copytree(src, dst, symlinks=False, ignore=None):
    '''
        shutil.copytree can't copy to existed destenition. We need the own analogue
    '''
    assert(src and dst)
    for path, dirs, files in os.walk(src, topdown=True):
        base = path[ len(src) if path.startswith(src) else 0 : ].strip('/')
        for d in dirs:
            dirname = os.path.join(dst, base, d)
            if not os.path.exists(dirname):
                os.mkdir(dirname)
            elif not os.path.isdir(dirname):
                RuntimeError("Path {} is exist and it isn't directory as expected".format(dirnmae))
        for f in files:
            shutil.copy(os.path.join(path, f), os.path.join(dst, base, f))
