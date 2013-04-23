What is Chewy?
==============

Chewy is a _CMake Helpers Easy Way sYnchronizer_.
Chewy was designed to help an expecienced programmers to manage [CMake](http://cmake.org) modules
in their projects (just like package managers do).
It allows to check versions of CMake modules and to keep their freshness by synchronizing
with a repository (or even few repositories), so you always have last versions of them in
all of your projects.

Motivation
==========

If you are an experienced developer who use CMake as a build-system in your daily work, you should
be close with such kind of a situation. You are developing a CMake module for your current project (it
could be a some specific library's finder or just some kind of helper). But some time latter you are
copying that module to another (possible just started) project. As a result, some black day you have
found yourself as an owner of a work-environment directory fulled of a great many of local copies of
different projects with tens of non-synchronized CMake modules inside. New ones have fresh versions.
But you would like to update versions of modules from more ancient ones.

There are situations also when you are coming back to an years ago abandoned project and injecting
some interesting changes in a rush of programming creativity. But day latter you are realizing what
such a brilliant find should be propagated to all other projects.

In moments like that, you could feel some unclear desire in your mind. It would be so great to keep
all of your modules (in an accurate sorted and classified way with tiny name tags attached to them)
in your own storage and just to have possibility to synchronize them from different projects!
A sharp programmer's brain are suggesting a possible solution. You can take all your modules away to
a separate VCS repository and plug it in as an 'external' one to you project's repository. You can…
but "Hey, Houston! We've have a problem here"! The repository contains a big number of files when you
need just a few of them in your project. Not to mention a complexity of external repositories' links
using with distributed version control systems. Long story short a laziness wins! Entropy of you
work directory are not decreasing with a threatening speed. And you are writing Christmas message to
Santa asking to have a simple package manager to manage your own cmake-modules as your Christmas
wish. But deep in you mind you know what in the morning you gonna find a Scottish jumper that was
bought by you wife in Macys last week…

Sounds familiar? So when we glad to introduce our charming shaggy second pilot to you — Chewy!


Usage
=====
to list repositorie's files by checking manifest

    $ chewy list [repo-URL ...]

As result you gonna see a list of filename, version and module description.


To add new module and all related files to your project tree or to roll back all changes of existed file to
repositorie's original one's condition

    $ chewy install file-URL ...


To delete installed module and all related files from your project tree. Note: this command doesn't
delete any of modules' directory's empty sub directories. This is user's responsibility.

    $ chewy uninstall file-PATH ...


to receive newest versions of your project's files by checking a repository

    $ chewy update [file-PATH ...]


to check availability of newest versions of your project's files

    $ chewy status [file-PATH ...]

As result you gonna see a list of

    *|U|M|D filename local-version remote-version

where,
- `*` - you have a last version of the module
- `U` - there is an **U**pdate 
- `M` - the local module was **M**odified
- `D` - there is no corresponded module on the repository


and finally... ;-)

    $ chewy jump-to-light-speed
    Uuuuuuuuuur Ahhhhhrrrrr
    Uhrrrrr Ahhhhrrrr
    Aaaaarhg...


Your own Chewy-repository
=========================
Lets image you have a few fancy CMake-modules, which you want to share between some of your
C++ projects, and GitHub repository named `https://github/solo/han-shot-first.git`. So:

    $ git clone https://github/solo/han-shot-first.git hsf
    $ cd hsf

Copy your modules to repository:

    $ cp ~/FindDroidsYouRLooking4.cmake .
    $ cp ~/order-66.cmake .

And a complex one, which has two additional files in subdirectory

    $ cp ~/ObiWanHelper.cmake .
    $ mkdir jedi-stuff
    $ cp ~/elegant-lightsaber.in jedi-stuff/
    $ cp ~/barbaric-blaster.in jedi-stuff/

Plsce them undere version control:

    git add *.cmake
    git add jedi-stuff
    git -a -m 'Repository init'

So, now you have three modules under version control, but it isn't Chewy-repository still.
What should you do is to add a few Chewy-tags to your modules, like this:

    $ for i in *.cmake; do \
        echo "X-Chewy-Repobase: https://raw.github/solo/han-shot-firs/master/" >> $i \
        echo "X-Chewy-Path: $i" >> $i \
        echo "X-Chewy-Version: 1.0" >> $i \
      done

And one extra tag, described dependent files, for complex module:

    $ for i in jedi-stuff/*; do
         echo "X-Chewy-AddonFile: $i" >> ObiWanHelper.cmake
      done

Note the variable `i` above contains a directory name as soon a a filename: `jedi-stuff/elegan-lightsaber.in`

At last, you have to give some descriptions for your modules:

    $ echo "X-Chewy-Description: Help me Obi-Wan Kenobi. You’re my only hope!"    >> ObiWanHelper.cmake
    $ echo "X-Chewy-Description: C3PO and R2D2 droid-libraries finder"            >> FindDroidsYouRLooking4.cmake
    $ echo "X-Chewy-Description: Add execute-order-66 target to you build system" >> order-66.cmake

And one last move — launch `chewy-update-manifest` util from Chewy package:

    $ chewy-update-manifest

That command gonna create a manifest file, so you want to add it under version control, fix all changes
and push it to origin repository finally:

    $ git add manifest
    $ git ci -a -m 'Chewy-repository is done'
    $ git push

Now you can use you fresh shiny Chwey-repository:

    $ chewy list https://raw.github/solo/han-shot-firs/master
    $ cd ~/work/dark-side-cxx-project/
    $ chewy add https://raw.github/solo/han-shot-firs/master/order-66.cmake

Or even:

    $ cd ~/work/rebel-alliance-cxx-senator/
    $ chewy add https://raw.github/solo/han-shot-firs/master/ObiWanHelper.cmake

And if you think some used modules have new version, you can just easy update it in any project:

    $ chewy status
    $ chewy update
q


> May the Force be with you!


How to get help
===============

    $ chewy --help
    $ chewy command --help
    $ man chewy # TODO


See also
========

* [Repository](https://github.com/mutanabbi/chewy-cmake-rep) of reusable CMake modules managed with `chewy`

>Chewy is the best second pilot ever!
