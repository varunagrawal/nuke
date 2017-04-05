#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main command line tool to nuke a directory."""
import os
import os.path as osp
import shutil
import argparse
from clint.textui import colored, puts, prompt


def nuke(directory):
    """Nuke the directory specified."""
    puts("Nuking " + colored.cyan(directory))
    try:
        # Nuke the directory
        # Just iterate over the contents and delete everything accordingly.
        for x in os.listdir(directory):
            t = osp.join(directory, x)
            if osp.isdir(t):
                shutil.rmtree(t)
            else:
                os.remove(t)

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
