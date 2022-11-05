#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main command line tool to nuke a directory."""

# pylint: disable=invalid-name,unused-variable

import errno
import fnmatch
import os
from pathlib import Path

import click
import crayons
from rich.progress import track

from .dirtree import get_dirtree
from .utils import parse_ignore_file


def get_file_list(directory):
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


def ignore_paths(path_list, ignore_patterns, process=str):
    """
    Go through the `path_list` and ignore any paths that match the patterns in `ignore_patterns`
    :param path_list: List of file/directory paths.
    :param ignore_patterns: List of nukeignore patterns.
    :param process: Function to apply to every element in the path list before performing match.
    :return: The updated path list
    """
    for pattern in ignore_patterns:
        path_list = [
            n for n in path_list if not fnmatch.fnmatch(process(n), pattern)
        ]
    return path_list


def list_files_tree(directory):
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


def delete(x):
    """
    Convenience method to delete file or directory.
    :param x: The filesystem object to delete.
    """
    if x.is_dir():
        # delete the directory
        try:
            # Check if directory is a symbolic link
            if x.is_symlink():
                x.unlink()
            else:
                # Just a regular delete
                x.rmdir()
        except (OSError, ):
            # This means the directory is not empty, so do nothing.
            # Possibly because an nukeignored file is in the directory.
            return

    else:
        # delete the file
        x.unlink()


def nuke(directory):
    """This is where all the nuking happens."""
    click.echo("Nuking " + crayons.cyan(directory))

    ### Nuke the directory

    # Just iterate over the contents and delete everything accordingly.
    file_list, ignore_patterns = get_file_list(directory)

    # Filter the file list based on the ignore patterns.
    nuke_list = ignore_paths(file_list, ignore_patterns)

    for x in track(nuke_list):
        try:
            delete(x)

        except (OSError, ) as ex:
            # file does not exist
            if ex.errno == errno.ENOENT:
                click.secho("Nuke target does not exist...", fg="red")
            else:
                click.secho(
                    "File exception {0}: {1}!".format(ex.errno, ex.strerror),
                    fg="red",
                )


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("directory", nargs=1, default=Path.cwd())
@click.option("-l",
              is_flag=True,
              default=False,
              help="List all the files that will be nuked")
@click.option("-y",
              is_flag=True,
              is_eager=True,
              default=False,
              help="Flag to confirm nuking")
def main(directory, l, y):
    """
    Nuke (aka delete the contents of) the DIRECTORY specified.
    Default directory is the current directory.
    """
    try:
        # expand and resolve the input directory path
        directory = Path(directory).expanduser().resolve(strict=True)
    except FileNotFoundError:
        click.secho(
            "Invalid directory specified. Please ensure directory is valid.",
            fg="red")

    if l:
        list_files_tree(directory=directory)
        return
    if y or click.confirm(
            "Are you sure you want to nuke directory " +
            crayons.blue(directory) + "?",
            default=True,  # sets the prompt to Y/n
            abort=False,
    ):
        nuke(directory)


if __name__ == "__main__":
    main(os.getcwd(), False, False)
