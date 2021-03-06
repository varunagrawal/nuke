"""Unit tests for nuke"""

# pylint: disable=invalid-name,unused-variable,unused-import,missing-docstring

import os
from pathlib import Path
import shutil

import pytest
from nuke import nuke

TEST_DIR = Path("test_directory")

NUKEIGNORE = Path('.nukeignore')


def setup():
    """Invoked each time before running a test."""
    try:
        TEST_DIR.mkdir()
    except (FileExistsError,):
        # if the test directory already exists then just continue.
        pass

    open((TEST_DIR / "random.py"), 'a').close()
    open((TEST_DIR / "another.py"), 'a').close()
    (TEST_DIR / 'ignore_dir').mkdir()
    open((TEST_DIR / 'ignore_file'), 'a').close()


def test_nuke_dir():
    nuke.nuke(TEST_DIR)
    assert os.listdir(TEST_DIR) == []


def test_nuke_current_dir():
    directory = (Path.cwd() / TEST_DIR)
    os.chdir(directory)
    nuke.nuke(Path.cwd())
    assert os.listdir(".") == []
    os.chdir("..")


def test_invalid_dir():
    nuke.nuke(TEST_DIR)
    nuke.nuke("invalid_dir")


def test_ignore_file():
    with open((TEST_DIR / NUKEIGNORE), 'w') as ni:
        ni.write("ignore_file")

    nuke.nuke(TEST_DIR)

    assert (TEST_DIR / 'ignore_file').exists()

    os.remove((TEST_DIR / NUKEIGNORE))
    os.remove((TEST_DIR / 'ignore_file'))


def test_ignore_directory():
    with open((TEST_DIR / NUKEIGNORE), 'w') as ni:
        ni.write("ignore_dir")

    open((TEST_DIR / 'ignore_dir' / 'file_inside_ignore_dir'), 'a').close()
    nuke.nuke(TEST_DIR)

    assert (TEST_DIR / 'ignore_dir').exists()
    assert (TEST_DIR / 'ignore_dir' / 'file_inside_ignore_dir').exists()

    # remove the whole directory in one fell swoop
    shutil.rmtree((TEST_DIR / 'ignore_dir'))
    os.remove((TEST_DIR / NUKEIGNORE))


def test_ignore_directory_with_slash():
    with open((TEST_DIR / NUKEIGNORE), 'w') as ni:
        ni.write("ignore_dir/")
    open((TEST_DIR / 'ignore_dir' / 'file_inside_ignore_dir'), 'a').close()
    nuke.nuke(TEST_DIR)

    assert (TEST_DIR / 'ignore_dir').exists()
    assert (TEST_DIR / 'ignore_dir' / 'file_inside_ignore_dir').exists()

    # remove the whole directory in one fell swoop
    shutil.rmtree((TEST_DIR / 'ignore_dir'))
    os.remove((TEST_DIR / NUKEIGNORE))


def test_nuke_list():
    os.mkdir((TEST_DIR / 'test_subdir'))
    open((TEST_DIR / 'test_subdir' / "subfile.txt"), 'a').close()

    # Create the nukeignore file
    with open((TEST_DIR / NUKEIGNORE), 'w') as ni:
        ni.writelines('\n'.join(["ignore_dir/", 'ignore_file']))

    import io
    from contextlib import redirect_stdout

    sio = io.StringIO()
    with redirect_stdout(sio):
        nuke_files = nuke.list_files_tree(TEST_DIR)
    output = sio.getvalue()

    # split output into separate lines
    output_lines = output.strip().split('\n')

    # Output should look something like this:
    # ├── test_subdir/
    # │   └── subfile.txt
    # ├── another.py
    # └── random.py
    expected_result = ("test_subdir/",
                       "subfile.txt",
                       "another.py",
                       "random.py")

    for path in output_lines:
        p = path.replace("├── ", "").replace("└── ", "").replace("│   ", "")
        assert p in expected_result

    # clean up the directory for the teardown
    nuke.nuke(TEST_DIR)


def teardown():
    """Invoke each time after running a test."""
    # os.rmdir(TEST_DIR)
    shutil.rmtree(TEST_DIR)  # remove the test directory
