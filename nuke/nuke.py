#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main command line tool to nuke a directory."""
import argparse
import fnmatch
import os
import os.path as osp
import shutil
from clint.textui import colored, puts, prompt


def parse_ignore_file(file):
    with open(file) as ignore_file:
        ignore_list = ignore_file.readlines()
    return ignore_list


def nuke(directory):
    """Nuke the directory specified."""
    puts("Nuking " + colored.cyan(directory))

    element_list = []
    ignore_patterns = []

    for (dirpath, dirnames, filenames) in os.walk(directory, topdown=False):
        element_list.extend([osp.join(dirpath, dn) for dn in dirnames])
        for fn in filenames:
            print(fn)
            if fn == ".nukeignore":
                print("Found a nukeignore at {}".format(osp.join(dirpath, fn)))
                ignore_patterns.extend(parse_ignore_file(osp.join(dirpath, fn)))
                continue
            element_list.append(osp.join(dirpath, fn))

    # if ".nukeignore" in element_list:
    #     with open(os.path.join(directory, ".nukeignore")) as nuke_ignore:
    #         ignore_patterns = nuke_ignore.readlines()
    #         element_list.remove(".nukeignore")

    try:
        # Nuke the directory
        # Just iterate over the contents and delete everything accordingly.
        print(element_list)
        print(ignore_patterns)
        # TODO figure out how to match patterns correctly
        for pattern in ignore_patterns:
            for f in element_list:
                print("Filename: {0}\tPattern: {1}".format(f, pattern))
                if fnmatch.fnmatch(f, pattern):
                    print("{0} matches {1}".format(f, pattern))
            element_list = [n for n in element_list if not fnmatch.fnmatch(n, pattern)]
        print(element_list)

        for x in element_list:
            t = osp.join(directory, x)
            # if
            # if osp.isdir(t):
            #     shutil.rmtree(t)
            # else:
            #     os.remove(t)

    except (FileNotFoundError,):
        puts(colored.yellow("Nuke target does not exist..."))
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
