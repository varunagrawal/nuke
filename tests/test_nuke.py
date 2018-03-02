import os
import os.path as osp
from nuke import nuke
import shutil
import pytest

test_dir = "test_directory"

NUKEIGNORE = '.nukeignore'


def setup():
    """Invoked each time before running a test."""
    os.mkdir(test_dir)
    open(osp.join(test_dir, "random.py"), 'a').close()
    open(osp.join(test_dir, "another.py"), 'a').close()
    os.mkdir(osp.join(test_dir, 'ignore_dir'))
    open(osp.join(test_dir, 'ignore_file'), 'a').close()


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
    nuke.nuke("invalid_dir")


def test_ignore_file():
    with open(osp.join(test_dir, NUKEIGNORE), 'w') as ni:
        ni.write("ignore_file")

    nuke.nuke(test_dir)

    assert os.path.exists(osp.join(test_dir, 'ignore_file'))

    os.remove(osp.join(test_dir, NUKEIGNORE))
    os.remove(osp.join(test_dir, 'ignore_file'))


def test_ignore_directory():
    with open(osp.join(test_dir, NUKEIGNORE), 'w') as ni:
        ni.write("ignore_dir/")
    open(osp.join(test_dir, 'ignore_dir', 'file_inside_ignore_dir'), 'a').close()
    nuke.nuke(test_dir)

    assert os.path.exists(osp.join(test_dir, 'ignore_dir'))
    assert os.path.exists(osp.join(test_dir, 'ignore_dir', 'file_inside_ignore_dir'))

    shutil.rmtree(osp.join(test_dir, 'ignore_dir'))  # remove the whole directory in one fell swoop
    os.remove(osp.join(test_dir, NUKEIGNORE))


def test_nuke_list():
    os.mkdir(osp.join(test_dir, 'test_subdir'))
    open(osp.join(test_dir, 'test_subdir', "subfile.txt"), 'a').close()

    # Create the nukeignore file
    with open(osp.join(test_dir, NUKEIGNORE), 'w') as ni:
        ni.writelines('\n'.join(["ignore_dir/", 'ignore_file']))

    nuke_files = nuke.list_files_tree(test_dir)

    for f in nuke_files:
        assert 'ignore' not in f['filename'].strip()

    # clean up the directory for the teardown
    nuke.nuke(test_dir)


def teardown():
    """Invoke each time after running a test."""
    # os.rmdir(test_dir)
    shutil.rmtree(test_dir)  # remove the test directory