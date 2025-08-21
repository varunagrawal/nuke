"""Unit tests for nuke"""

# pylint: disable=invalid-name,unused-variable,unused-import,missing-docstring,unspecified-encoding,redefined-outer-name

import io
import os
from contextlib import redirect_stdout
from pathlib import Path

from nuke import nuke

NUKEIGNORE = Path('.nukeignore')


def test_delete_nonempty_directory(base_directory):
    # Create sample directory to delete
    sample_dir = base_directory / 'sample_dir'
    sample_dir.mkdir()

    # Make directory non-empty
    open((sample_dir / 'sample_file'), 'a').close()

    assert not nuke.delete(
        sample_dir), "Non-empty directory didn't get deleted"


def test_nuke_dir(directory):
    nuke.nuke(directory)
    assert os.listdir(directory) == []


def test_nuke_current_dir(directory):
    directory = Path.cwd() / directory
    os.chdir(directory)
    nuke.nuke(Path.cwd())
    assert os.listdir(".") == []
    os.chdir("..")


def test_invalid_file(directory, capsys):
    nuke.delete(directory / "this_file_doesnt.exist")
    captured = capsys.readouterr()
    assert captured.out == "Nuke target does not exist...\n"


def test_invalid_dir(directory):
    nuke.nuke(directory)
    nuke.nuke("invalid_dir")


def test_ignore_file(directory):
    with open((directory / NUKEIGNORE), 'w') as ni:
        ni.write("ignore_file")

    nuke.nuke(directory)

    assert (directory / 'ignore_file').exists()


def test_ignore_directory(directory):
    with open((directory / NUKEIGNORE), 'w') as ni:
        ni.write("ignore_dir")

    open((directory / 'ignore_dir' / 'file_inside_ignore_dir'), 'a').close()
    nuke.nuke(directory)

    assert (directory / 'ignore_dir').exists()
    assert (directory / 'ignore_dir' / 'file_inside_ignore_dir').exists()


def test_ignore_directory_with_slash(directory):
    with open((directory / NUKEIGNORE), 'w') as ni:
        ni.write("ignore_dir/")

    open((directory / 'ignore_dir' / 'file_inside_ignore_dir'), 'a').close()
    nuke.nuke(directory)

    assert (directory / 'ignore_dir').exists()
    assert (directory / 'ignore_dir' / 'file_inside_ignore_dir').exists()


def test_nuke_list(directory):
    os.mkdir((directory / 'test_subdir'))
    open((directory / 'test_subdir' / "subfile.txt"), 'a').close()

    # Create the nukeignore file
    with open((directory / NUKEIGNORE), 'w') as ni:
        ni.writelines('\n'.join(["ignore_dir/", 'ignore_file']))

    sio = io.StringIO()
    with redirect_stdout(sio):
        nuke.list_files_tree(directory)
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
    nuke.nuke(directory)
