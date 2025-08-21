#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main command line tool to nuke a directory."""

# pylint: disable=invalid-name,unused-variable

import errno
import fnmatch
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

import click
import crayons
from rich.progress import track

from nuke.dirtree import get_dirtree
from nuke.utils import parse_ignore_file


def get_file_list(directory: Path) -> Tuple[List[Path], List[str]]:
    """
    Retrieve all the files in the directory tree that are to be nuked,
    as well as the list of file patterns to ignore.
    :param directory: The root directory of the directory tree to nuke.
    :return: The list of all files to be deleted and the list of all ignore patterns.
    """
    file_list = []
    ignore_patterns = []

    # Get the list of all the files/dirs in the directory to nuke.
    # We traverse in a bottom up manner so that directory removal is trivial.
    for (dirpath, dirnames, filenames) in os.walk(directory, topdown=False):
        dirpath = Path(dirpath)
        file_list.extend([(dirpath / dn) for dn in dirnames])

        for fn in filenames:
            if fn == ".nukeignore":
                ignore_patterns.extend(
                    parse_ignore_file((dirpath / fn), dirpath))
                continue
            file_list.append((dirpath / fn))

    return file_list, ignore_patterns


def ignore_paths(
    path_list: List[Dict[str, Any]],
    ignore_patterns: List[str],
    processor: Callable = str,
) -> List[Dict[str, Any]]:
    """
    Go through the `path_list` and ignore any paths that match the patterns in `ignore_patterns`
    :param path_list: List of file/directory paths.
    :param ignore_patterns: List of nukeignore patterns.
    :param processor: Function to apply to every element in the path list before performing match.
    :return: The updated path list
    """
    for pattern in ignore_patterns:
        path_list = [
            n for n in path_list if not fnmatch.fnmatch(processor(n), pattern)
        ]
    return path_list


def list_files_tree(directory: Path) -> List[Dict[str, Any]]:
    """
    List all the files to be nuked in a nice directory tree.
    :param directory: The root directory to list from.
    :return: The list of files to be nuked. Each element of the list is a dict of filename and path.
    """
    # seperate function to get the dirtree to make the code more legible
    file_list, ignore_patterns = get_dirtree(directory)

    # Filter the nuke list based on the ignore patterns.
    file_list = ignore_paths(file_list, ignore_patterns,
                             lambda x: str(x["path"]))

    # Get the indented filenames only for printing
    file_tree = [str(x["repr"]) for x in file_list]

    for f in file_tree:
        click.echo(f)

    return file_list


def delete(x: Path) -> None:
    """Convenience method to delete file or directory.

    Args:
        x (Path): The filesystem object to delete.
    """
    if x.is_dir():
        # delete the directory
        try:
            x.rmdir()
        except (OSError, ):
            # This means the directory is not empty, so do nothing.
            # Possibly because a `nukeignore`d file is in the directory.
            click.secho(
                f"Directory {x} is not empty, perhaps there is an ignored file in it?",
                fg="red",
            )
            return

    else:
        try:
            # delete the file
            x.unlink()

        except (OSError, ) as ex:
            # file does not exist
            if ex.errno == errno.ENOENT:
                click.secho("Nuke target does not exist...", fg="red")
            else:  # pragma: no cover
                click.secho(
                    f"File exception {ex.errno}: {ex.strerror}!",
                    fg="red",
                )


def nuke(directory: Path) -> None:
    """This is where all the nuking happens."""
    click.echo("Nuking " + crayons.cyan(directory))

    ### Nuke the directory

    # Just iterate over the contents and delete everything accordingly.
    file_list, ignore_patterns = get_file_list(directory)

    # Filter the file list based on the ignore patterns.
    nuke_list = ignore_paths(file_list, ignore_patterns)

    for x in track(nuke_list):
        delete(x)
