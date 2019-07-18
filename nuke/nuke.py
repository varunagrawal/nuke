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


def parse_ignore_file(filename, dirname):
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

            pattern = str(dirname / x)
            # check if pattern is a directory
            if x[-1] == '/':
                pattern += '/'

            # little hack to make sure directories and their contents are included
            # since fnmatch only matches filenames and not directory contents directly.
            if pattern[-1] == '/':  # we have a directory
                # add the pattern without the trailing slash to match the directory
                ignore_list.append(pattern[:-1])
                pattern += '*'  # create pattern for all paths inside directory
            ignore_list.append(pattern)

    return ignore_list


def get_dirtree(directory):
    """
    Get the directory tree of the `directory`.
    :param directory: The root directory from where to generate the directory tree.
    :return: The list of paths with appropriate indenting
    """
    element_list = []
    ignore_patterns = []

    # Get the list of all the files/dirs in the directory to nuke.
    # We traverse in a bottom up manner so that directory removal is trivial.
    for (dirpath_str, dirnames, filenames) in os.walk(directory):
        level = dirpath_str.replace(str(directory), '').count(os.sep)
        indent = ' ' * 4 * level

        dirpath = Path(dirpath_str)

        # We record every element in the tree as a dict of the indented name (repr)
        # and the path so we can use the ignore methods on the paths and still
        # have the indented names for our tree

        # Add the current directory
        element = {
            'repr': '{}{}/'.format(indent, dirpath.name),
            'path': dirpath
        }
        element_list.append(element)

        subindent = ' ' * 4 * (level + 1)
        # Add the files in the directory
        for fn in filenames:
            if fn == ".nukeignore":
                ignore_patterns.extend(parse_ignore_file((dirpath / fn),
                                                         dirpath))
                continue

            element = {
                'repr': "{}{}".format(subindent, fn),
                'path': (dirpath / fn)
            }
            element_list.append(element)

    return element_list, ignore_patterns


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
                ignore_patterns.extend(parse_ignore_file((dirpath / fn),
                                                         dirpath))
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
        path_list = [n for n in path_list if not fnmatch.fnmatch(process(n),
                                                                 pattern)]
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
    file_list = ignore_paths(file_list, ignore_patterns, lambda x: str(x['path']))

    # Get the indented filenames only for printing
    file_tree = [x['repr'] for x in file_list]

    for f in file_tree:
        # click formats the filename to the absolute path
        click.echo(crayons.white(click.format_filename(f)))

    return file_list


def delete(x):
    """
    Convenience method to delete file or directory.
    :param x: The filesystem object to delete.
    """
    if x.is_dir():
        # delete the directory
        try:
            x.rmdir()
        except (OSError,):
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

    with click.progressbar(nuke_list, length=len(nuke_list)) as nuke_l:
        for x in nuke_l:
            try:
                delete(x)

            except (OSError,) as ex:
                # file does not exist
                if ex.errno == errno.ENOENT:
                    click.secho("Nuke target does not exist...", fg='red')
                else:
                    click.secho("File exception {0}: {1}!".format(ex.errno, ex.strerror),
                                fg='red')


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('directory', nargs=1, default=Path.cwd())
@click.option('-l', is_flag=True, default=False, help="List all the files that will be nuked")
@click.option('-y', is_flag=True, is_eager=True, default=False, help="Flag to confirm nuking")
def main(directory, l, y):
    """
    Nuke (aka delete the contents of) the DIRECTORY specified.
    Default directory is the current directory.
    """
    try:
        # expand and resolve the input directory path
        directory = Path(directory).expanduser().resolve(strict=True)
    except FileNotFoundError:
        click.secho("Invalid directory specified. Please ensure directory is valid.", fg='red')

    if l:
        list_files_tree(directory=directory)
        return
    if y or \
        click.confirm("Are you sure you want to nuke directory " + crayons.blue(directory) + "?",
                      default=True,  # sets the prompt to Y/n
                      abort=False):
        nuke(directory)


if __name__ == "__main__":
    main(os.getcwd(), False, False)
