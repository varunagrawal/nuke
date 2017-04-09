#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main command line tool to nuke a directory."""
import argparse
import errno
import fnmatch
import os
import os.path as osp
from clint.textui import colored, puts, prompt


def parse_ignore_file(filename, dirname):
    """
    Parse the ignore file and return a list of ignore patterns. 
    Each pattern has the complete file path so we can take into account ignore at different levels. 
    :param filename: The name of the ignore file.
    :param dirname: The directory name where the ignore file was found. 
    :return: List of ignore patterns.
    """
    with open(filename) as ignore_file:
        ignore_list = [osp.join(dirname, x.strip()) for x in ignore_file.readlines()]
    return ignore_list


def nuke(directory):
    """Nuke the directory specified."""
    puts("Nuking " + colored.cyan(directory))

    element_list = []
    ignore_patterns = []

    # Get the list of all the files/dirs in the directory to nuke.
    # We traverse in a bottom up manner so that directory removal is trivial.
    for (dirpath, dirnames, filenames) in os.walk(directory, topdown=False):
        element_list.extend([osp.join(dirpath, dn) for dn in dirnames])
        for fn in filenames:
            if fn == ".nukeignore":
                ignore_patterns.extend(parse_ignore_file(osp.join(dirpath, fn), dirpath))
                continue
            element_list.append(osp.join(dirpath, fn))

    try:
        # Nuke the directory
        # Just iterate over the contents and delete everything accordingly.
        nuke_list = list(element_list)
        # Filter the nuke list based on the ignore patterns.
        for pattern in ignore_patterns:
            nuke_list = [n for n in nuke_list if not fnmatch.fnmatch(n, pattern)]

        for x in nuke_list:
            if osp.isdir(x):
                try:
                    os.rmdir(x)
                except (OSError,):
                    # This means the directory is not empty.
                    # Possibly because an ignored file is in the directory.
                    continue
            else:
                os.remove(x)

    except (OSError,) as ex:
        if ex.errno == errno.ENOENT:
            puts(colored.yellow("Nuke target does not exist..."))
        else:
            puts(colored.red("File based {0} exception! Please report on Github.".format(ex.errno)))
    except (Exception,):
        puts(colored.yellow("Nuking failed..."))


def _argparse():
    parser = argparse.ArgumentParser("nuke")
    parser.add_argument("directory",
                        nargs='?',
                        default=os.getcwd(),
                        help="Directory to nuke! Default is current directory")
    parser.add_argument("-y", help="Confirm nuking", action="store_true")
    args = parser.parse_args()
    return args


def main():
    """The main function where it all starts."""
    args = _argparse()
    directory = osp.abspath(args.directory)
    if args.y or prompt.yn("Are you sure you want to nuke directory " + colored.blue(directory) + "?"):
        nuke(directory)


if __name__ == "__main__":
    main()
