#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utilities for getting directory tree."""

import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

from nuke.utils import fg, get_colorized, parse_ignore_file


def get_dirtree(directory: Path) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Get the directory tree of the `directory`.
    :param directory: The root directory from where to generate the directory tree.
    :return: The list of paths with appropriate indenting, and the list of ignore patterns.
    """
    element_list = []
    ignore_patterns = []

    file_link = fg("├── ", 241)  # u'\u251c\u2500\u2500 '
    last_file_link = fg("└── ", 241)  # u'\u2514\u2500\u2500 '
    tree_branch = fg("│   ", 241)  # u'\u2502   '

    # Get the list of all the files/dirs in the directory to nuke.
    # We traverse in a bottom up manner so that directory removal is trivial.
    for (dirpath_str, _, filenames) in os.walk(directory, topdown=False):
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
                "repr": f"{indent}{get_colorized(dirpath)}/",
                "path": dirpath,
            }
            element_list.append(element)

        subindent = tree_branch * (level)
        # Add the files in the directory
        for idx, fn in enumerate(filenames):
            if fn == ".nukeignore":
                ignore_patterns.extend(
                    parse_ignore_file((dirpath / fn), dirpath))
                continue

            # Check if it is the last element
            if idx == len(filenames) - 1:
                branch = subindent + last_file_link
            else:
                branch = subindent + file_link

            element = {
                "repr": f"{branch}{ get_colorized(dirpath / fn)}",
                "path": (dirpath / fn),
            }
            element_list.append(element)

    return element_list, ignore_patterns
