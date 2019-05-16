"""Unit tests for nuke"""

# pylint: disable=invalid-name,unused-variable,unused-import,missing-docstring

import os
import os.path as osp
import shutil

import pytest
from nuke import nuke

TEST_DIR = "test_directory"

NUKEIGNORE = '.nukeignore'


def setup():
    """Invoked each time before running a test."""
    try:
        os.mkdir(TEST_DIR)
    except (FileExistsError,):
        # if the test directory already exists then just continue.
        pass

    open(osp.join(TEST_DIR, "random.py"), 'a').close()
    open(osp.join(TEST_DIR, "another.py"), 'a').close()
    os.mkdir(osp.join(TEST_DIR, 'ignore_dir'))
    open(osp.join(TEST_DIR, 'ignore_file'), 'a').close()


def test_nuke_dir():
    nuke.nuke(TEST_DIR)
    assert os.listdir(TEST_DIR) == []


def test_nuke_current_dir():
    directory = osp.join(os.getcwd(), TEST_DIR)
    os.chdir(directory)
    nuke.nuke(os.getcwd())
    assert os.listdir(".") == []
    os.chdir("..")


def test_invalid_dir():
    nuke.nuke(TEST_DIR)
    nuke.nuke("invalid_dir")


def test_ignore_file():
    with open(osp.join(TEST_DIR, NUKEIGNORE), 'w') as ni:
        ni.write("ignore_file")

    nuke.nuke(TEST_DIR)

    assert os.path.exists(osp.join(TEST_DIR, 'ignore_file'))

    os.remove(osp.join(TEST_DIR, NUKEIGNORE))
    os.remove(osp.join(TEST_DIR, 'ignore_file'))


def test_ignore_directory():
    with open(osp.join(TEST_DIR, NUKEIGNORE), 'w') as ni:
        ni.write("ignore_dir/")
    open(osp.join(TEST_DIR, 'ignore_dir', 'file_inside_ignore_dir'), 'a').close()
    nuke.nuke(TEST_DIR)

    assert os.path.exists(osp.join(TEST_DIR, 'ignore_dir'))
    assert os.path.exists(osp.join(TEST_DIR, 'ignore_dir', 'file_inside_ignore_dir'))

    shutil.rmtree(osp.join(TEST_DIR, 'ignore_dir'))  # remove the whole directory in one fell swoop
    os.remove(osp.join(TEST_DIR, NUKEIGNORE))


def test_nuke_list():
    os.mkdir(osp.join(TEST_DIR, 'test_subdir'))
    open(osp.join(TEST_DIR, 'test_subdir', "subfile.txt"), 'a').close()

    # Create the nukeignore file
    with open(osp.join(TEST_DIR, NUKEIGNORE), 'w') as ni:
        ni.writelines('\n'.join(["ignore_dir/", 'ignore_file']))

    nuke_files = nuke.list_files_tree(TEST_DIR)

    for f in nuke_files:
        assert 'ignore' not in f['filename'].strip()

    # clean up the directory for the teardown
    nuke.nuke(TEST_DIR)


def teardown():
    """Invoke each time after running a test."""
    # os.rmdir(TEST_DIR)
    shutil.rmtree(TEST_DIR)  # remove the test directory
