# What is Chewy?
Chewy is a CMake Helpers Easy Way sYnchronizer
Chewy was deigned as a part of C++/Python projects' build system manager. It allows to check versions of cmake-helpers and to keep their freshness by synchronizing with a central repository, so you always have last versions of them in all of your projects.

# Chewy sounds so strange! How to communicate with him? What commands he accept?
to list repositorie's files by checking manifest
`chewy list [URL1 ...]`
As result you gonna see a list of
   filename version description

to add new file to your project tree or to roll back all changes of existed file to repositorie's original one's condition
`chewy get file-URL ...`

to receive newest versions of your project's files by checking a repository
`chewy update [file-URL ...]`

to check availability of newest versions of your project's files
`chewy status [file-URL ...]`
As result you gonna see a list of
   U|M filename LocalVersion RemoteVersion
U - for Update
M - for Modified


>Chewy is the best second pilot ever!
