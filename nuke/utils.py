#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utilities module."""


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
