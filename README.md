What is Chewy?
==============

Chewy is a CMake Helpers Easy Way sYnchronizer
Chewy was deigned as a part of C++/Python projects' CMake-based build system manager.
It allows to check versions of CMake modules and to keep their freshness by synchronizing
with a central repository, so you always have last versions of them in all of your projects.

Motivation
==========
If you are an experienced developer who use cmake-based build-system in your daily work, you should
be close with such kind of situation. You are developing a cmake-module for your current project (it
could be a some specific library's finder or just some kind of helper). But some time latter you are
copying that module to just created project. As a result, some black day you have found yourself as
an owner of a work-environment directory fulled of a great many of local copies of different projects
with tens of non-synchronized cmake-modules inside. New ones have fresh versions. But you would like
to update versions of modules from more ancient ones.

There are situations also when you are coming back to an years ago abandoned project and injecting
some interesting changes in a rush of programming creativity. But day latter you are realizing what
such a brilliant find should be propagated to all other projects.

In moments like that you could feel some unclear desire in your mind. It would be so great to keep
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

    chewy list [URL1 ...]

As result you gonna see a list of filename, version and module description.


To add new file to your project tree or to roll back all changes of existed file to repositorie's
original one's condition

    chewy get file-URL ...


to receive newest versions of your project's files by checking a repository

    chewy update [file-URL ...]


to check availability of newest versions of your project's files

    chewy status [file-URL ...]

As result you gonna see a list of

    U|M filename LocalVersion RemoteVersion

**U** - for **U**pdate
**M** - for **M**odified


    chewy jump-to-light-speed
      Uuuuuuuuuur Ahhhhhrrrrr
      Uhrrrrr Ahhhhrrrr
      Aaaaarhg...


How to get help
===============
chewy --help
chewy command --help
man chewy


>Chewy is the best second pilot ever!
