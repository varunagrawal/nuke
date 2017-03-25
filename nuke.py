#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main command line tool to nuke a directory.
"""
import os
import os.path as osp
import shutil
import argparse
from clint.textui import colored, puts, prompt


def nuke(directory):
    puts("Nuking " + colored.cyan(directory))
        
    try:
        # Go to the parent directory
        os.chdir(osp.basename(directory))
        puts(osp.dirname(directory))

        # Nuke the directory
        shutil.rmtree(directory)
        os.mkdir(directory)
    except (FileNotFoundError,):
        puts(colored.yellow("Nuke target does not exist..."))
    except (Exception,):
        puts(colored.yellow("Nuking failed..."))


def _argparse():
    parser = argparse.ArgumentParser("nuke")
    parser.add_argument("directory", nargs='?', default=os.getcwd(), help="Directory to nuke! Default is current working directory")
    parser.add_argument("-y", help="Confirm nuking", action="store_true")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = _argparse()
    directory = osp.abspath(args.directory)
    if prompt.yn("Are you sure you want to nuke this directory?"):
        nuke(directory)
