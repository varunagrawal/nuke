import os
import os.path as osp
from nuke import nuke
import pytest

test_dir = "test"


def setup():
    """Invoked each time before running a test."""
    os.mkdir(test_dir)
    open(osp.join(test_dir, "random.py"), 'a').close()
    open(osp.join(test_dir, "another.py"), 'a').close()


def test_nuke_dir():
    nuke.nuke(test_dir)
    assert os.listdir(test_dir) == []


def test_nuke_current_dir():
    directory = osp.join(os.getcwd(), test_dir)
    os.chdir(directory)
    nuke.nuke(os.getcwd())
    assert os.listdir(".") == []
    os.chdir("..")


def test_invalid_dir():
    nuke.nuke(test_dir)
    nuke.nuke("invalid")


def test_nuke_list():
    files, ignore_patterns = nuke.get_file_list(test_dir)
    for f in os.listdir(test_dir):
        assert str(osp.join(test_dir, f)) in files
    # clean up the directory for the teardown
    nuke.nuke(test_dir)


def teardown():
    """Invoke each time after running a test."""
    os.rmdir(test_dir)
