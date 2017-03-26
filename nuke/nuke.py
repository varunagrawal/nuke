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

        # If we have to nuke the current directory,
        # we simply delete all the contents of the directory
        if directory == os.getcwd():
            for x in os.listdir(directory):
                t = osp.join(directory, x)
                if osp.isdir(t):
                    shutil.rmtree(t)
                else:
                    os.remove(t)

        # Deleting a specified directory is easier,
        # but we have to create the directory again
        else:
            shutil.rmtree(directory)
            os.mkdir(directory)

    except (FileNotFoundError,):
        puts(colored.yellow("Nuke target does not exist..."))
    except (Exception,) as ex:
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
    if args.y or \
    prompt.yn("Are you sure you want to nuke directory" +
              colored.blue(directory) + "?"):
        nuke(directory)


if __name__ == "__main__":
    main()
