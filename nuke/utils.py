"""Utilities module."""

from pathlib import Path
from typing import List

import crayons


def fg(text: str, color) -> str:
    """Set text to foregound color."""
    return f"\33[38;5;{color}m{text}\33[0m"


def bg(text: str, color) -> str:
    """Set text to background color."""
    return f"\33[48;5;{color}m{text}\33[0m"


def get_colorized(path: Path):
    """Colorize path name based on type."""
    name = path.name
    if path.is_dir():
        return crayons.blue(name)
    elif path.is_file():
        return crayons.green(name)
    elif path.is_mount():  # pragma: no cover
        return crayons.red(name)
    elif path.is_symlink():
        return crayons.cyan(name)
    elif path.is_socket():  # pragma: no cover
        return crayons.magenta(name)
    else:  # pragma: no cover
        return crayons.white(name)


def parse_ignore_file(filename: str, dirname: Path) -> List[str]:
    """
    Parse the ignore file and return a list of ignore patterns.
    Each pattern has the complete file path so we can take into account ignore at different levels.
    :param filename: The name of the ignore file.
    :param dirname: The directory Path where the ignore file was found.
    :return: List of ignore patterns.
    """
    ignore_list = []
    with open(filename) as ignore_file:
        for x in ignore_file.readlines():
            x = x.strip()

            # ignore if line is blank or a comment
            if x == "" or x[0] == "#":
                continue

            path = dirname / x

            pattern = str(path)

            # check if pattern is a directory
            # this is a little hack to make sure directories and their contents are included
            # since fnmatch only matches filenames and not directory contents directly.
            if path.is_dir():
                pattern += "/"

                # add the pattern without the trailing slash to match the directory
                ignore_list.append(pattern[:-1])
                pattern += "*"  # create pattern for all paths inside directory

            ignore_list.append(pattern)

    return ignore_list
