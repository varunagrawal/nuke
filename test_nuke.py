import os
import os.path as osp
from nuke import nuke
import pytest


def setup():
    """Invoked each time before running a test."""
    os.mkdir("test")
    open(osp.join("test", "random.py"), 'a').close()


def test_nuke_dir():
    nuke.nuke("test")
    assert os.listdir("test") == []


def test_nuke_current_dir():
    directory = osp.join(os.getcwd(), "test")
    os.chdir(directory)
    nuke.nuke(os.getcwd())
    assert os.listdir(".") == []
    os.chdir("..")


def test_invalid_dir():
    nuke.nuke("test")
    nuke.nuke("invalid")


def teardown():
    """Invoke each time after running a test."""
    os.rmdir("test")
