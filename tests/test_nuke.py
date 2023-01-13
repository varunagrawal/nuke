"""Unit tests for nuke"""

# pylint: disable=invalid-name,unused-variable,unused-import,missing-docstring,unspecified-encoding,redefined-outer-name

import io
import os
import shutil
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from nuke import nuke

NUKEIGNORE = Path('.nukeignore')


@pytest.fixture
def test_directory():
    """Invoked each time before running a test."""
    TEST_DIR = Path("test_directory")
    try:
        TEST_DIR.mkdir()
    except (FileExistsError, ):
        # if the test directory already exists then just continue.
        pass

    open((TEST_DIR / "random.py"), 'a').close()
    open((TEST_DIR / "another.py"), 'a').close()
    (TEST_DIR / 'ignore_dir').mkdir()
    open((TEST_DIR / 'ignore_file'), 'a').close()
    open((TEST_DIR / 'ignore_file'), 'a').close()
    Path(TEST_DIR / "symlink_file").symlink_to(TEST_DIR / "random.py")
    Path(TEST_DIR / "symlink_dir").symlink_to(TEST_DIR / "ignore_dir")

    yield TEST_DIR

    # remove the test directory
    shutil.rmtree(TEST_DIR)


def test_nuke_dir(test_directory):
    nuke.nuke(test_directory)
    assert os.listdir(test_directory) == []


def test_nuke_current_dir(test_directory):
    directory = (Path.cwd() / test_directory)
    os.chdir(directory)
    nuke.nuke(Path.cwd())
    assert os.listdir(".") == []
    os.chdir("..")


def test_invalid_dir(test_directory):
    nuke.nuke(test_directory)
    nuke.nuke("invalid_dir")


def test_ignore_file(test_directory):
    with open((test_directory / NUKEIGNORE), 'w') as ni:
        ni.write("ignore_file")

    nuke.nuke(test_directory)

    assert (test_directory / 'ignore_file').exists()


def test_ignore_directory(test_directory):
    with open((test_directory / NUKEIGNORE), 'w') as ni:
        ni.write("ignore_dir")

    open((test_directory / 'ignore_dir' / 'file_inside_ignore_dir'),
         'a').close()
    nuke.nuke(test_directory)

    assert (test_directory / 'ignore_dir').exists()
    assert (test_directory / 'ignore_dir' / 'file_inside_ignore_dir').exists()


def test_ignore_directory_with_slash(test_directory):
    with open((test_directory / NUKEIGNORE), 'w') as ni:
        ni.write("ignore_dir/")

    open((test_directory / 'ignore_dir' / 'file_inside_ignore_dir'),
         'a').close()
    nuke.nuke(test_directory)

    assert (test_directory / 'ignore_dir').exists()
    assert (test_directory / 'ignore_dir' / 'file_inside_ignore_dir').exists()


def test_nuke_list(test_directory):
    os.mkdir((test_directory / 'test_subdir'))
    open((test_directory / 'test_subdir' / "subfile.txt"), 'a').close()

    # Create the nukeignore file
    with open((test_directory / NUKEIGNORE), 'w') as ni:
        ni.writelines('\n'.join(["ignore_dir/", 'ignore_file']))

    sio = io.StringIO()
    with redirect_stdout(sio):
        nuke_files = nuke.list_files_tree(test_directory)
    output = sio.getvalue()

    # split output into separate lines
    output_lines = output.strip().split('\n')

    # Output should look something like this:
    # ├── test_subdir/
    # │   └── subfile.txt
    # ├── another.py
    # └── random.py
    expected_result = ("test_subdir/", "subfile.txt", "another.py",
                       "random.py", "symlink_file", "symlink_dir")

    for path in output_lines:
        p = path.replace("├── ", "").replace("└── ", "").replace("│   ", "")
        assert p in expected_result

    # clean up the directory for the teardown
    nuke.nuke(test_directory)
