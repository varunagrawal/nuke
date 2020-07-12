#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utilities for getting directory tree."""

import os
from pathlib import Path

import crayons

from .utils import parse_ignore_file


def fg(text, color):
    """Set text to foregound color."""
    return "\33[38;5;" + str(color) + "m" + text + "\33[0m"


def bg(text, color):
    """Set text to background color."""
    return "\33[48;5;" + str(color) + "m" + text + "\33[0m"


def get_colorized(path: Path):
    """Colorize path name based on type."""
    name = path.name
    if path.is_dir():
        return crayons.blue(name)
    elif path.is_file():
        return crayons.green(name)
    elif path.is_mount():
        return crayons.red(name)
    elif path.is_symlink():
        return crayons.cyan(name)
    elif path.is_socket():
        return crayons.magenta(name)
    else:
        return crayons.white(name)


def get_dirtree(directory):
    """
    Get the directory tree of the `directory`.
    :param directory: The root directory from where to generate the directory tree.
    :return: The list of paths with appropriate indenting
    """
    element_list = []
    ignore_patterns = []

    file_link = fg("|—— ", 241)
    tree_branch = fg("|  ", 241)

    # Get the list of all the files/dirs in the directory to nuke.
    # We traverse in a bottom up manner so that directory removal is trivial.
    for (dirpath_str, dirnames, filenames) in os.walk(directory):
        level = dirpath_str.replace(str(directory), "").count(os.sep)
        if level > 0:
            indent = tree_branch * (level - 1) + file_link
        else:
            indent = ""

        dirpath = Path(dirpath_str)

        # We record every element in the tree as a dict of the indented name (repr)
        # and the path so we can use the ignore methods on the paths and still
        # have the indented names for our tree

        # only add current directory as element to be nuked if no .nukeignore file is present
        if ".nukeignore" not in filenames:
            # Add the current directory
            element = {
                "repr": "{}{}/".format(indent, get_colorized(dirpath)),
                "path": dirpath,
            }
            element_list.append(element)

        subindent = tree_branch * (level) + file_link
        # Add the files in the directory
        for fn in filenames:
            if fn == ".nukeignore":
                ignore_patterns.extend(
                    parse_ignore_file((dirpath / fn), dirpath))
                continue

            element = {
                "repr": "{}{}".format(subindent, get_colorized(dirpath / fn)),
                "path": (dirpath / fn),
            }
            element_list.append(element)

    return element_list, ignore_patterns
