# Nuke


[![version](https://img.shields.io/pypi/v/nuke.svg)](https://pypi.python.org/pypi/nuke)
[![license](https://img.shields.io/pypi/l/nuke.svg)](https://pypi.python.org/pypi/nuke)
[![wheel](https://img.shields.io/pypi/wheel/nuke.svg)](https://pypi.python.org/pypi/nuke)
[![python](https://img.shields.io/pypi/pyversions/nuke.svg)](https://pypi.python.org/pypi/nuke)
[![say-thanks](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/varunagrawal)

Command line tool for nuking a directory 💥.

## Installation

Installing ``nuke`` is intended to be super easy. The only dependency is a supported Python interpreter. You can get ``nuke`` via ``pip``:

```shell
$ pip install nuke
```
``nuke`` is supported for Python versions 2.7, 3.5 & 3.6+.


## Usage

The most common usage of ``nuke`` is when you wish to recreate a build directory for a build program such as CMake.

To use ``nuke``, you just call :code:`nuke` from the command line and specify the directory you wish to nuke: 

```shell
$ nuke path/to/directory
```

If you are already in the directory you wish to nuke, you don't need to exit the directory. Calling :code:`nuke` without any arguments will nuke the current directory:

```shell
$ nuke  # same as "nuke ."
```

Since nuking is a dangerous operation and you don't want to inadvertently delete something important, `nuke` always asks you to confirm the nuking of a directory. If you wish to override this since you know what you are doing or you wish to use ``nuke`` in a shell script, you can pass in the ``-y`` flag:

```shell
$ nuke -y /path/to/dir/
```

You can also specify a ``.nukeignore`` file inside the directory to be nuked. This works similar to the ``.gitignore`` file. Every file that matches a pattern in the ``.nukeignore`` is ignored and spared from a gruesome fate of its eligible siblings.

For example:
```shell
*.py
```
will result in all ``.py`` files not being nuked.

Suppose you just want to see what files will be nuked without actually deleting them, you can then run ``nuke -l /path/to/dir``, and this will print out the directory tree of all the files that will be nuked.


### Version History

##### 2.2.1

Fixed bug in the `-l` list functionality so that ignored files are not displayed.

##### 2.2.0

Major bugfix in the ``.nukeignore`` functionality. ``nuke`` now ignores whole directories if the pattern ends in a slash (``/``).
Also, ``-l`` prints out files as a directory tree.

##### 2.1.1

Updated Python Trove Classifiers.

##### 2.1.0

Migrated from ``clint`` to ``click`` to streamline code. Added ``-l`` flag to list files that will be deleted without deleting them.

##### 2.0.0

Added feature to ignore files to nuke based on a ``.nukeignore`` file on a per directory level.

##### 1.0.5

Minor bug fixes.

##### 1.0

Nuke is out!