import shutil
from pathlib import Path

import pytest


@pytest.fixture(name="base_directory")
def base_directory_fixture():
    """Base directory which is passed to various tests."""
    directory = Path("test_directory")

    try:
        directory.mkdir()
    except (FileExistsError, ):
        # if the test directory already exists then just continue.
        pass

    yield directory

    # remove the test directory
    shutil.rmtree(directory)


@pytest.fixture(name="directory")
def directory_fixture(base_directory):
    """Invoked each time before running a test."""

    open(base_directory / "random.py", 'a').close()
    open(base_directory / "another.py", 'a').close()
    (base_directory / 'ignore_dir').mkdir()
    open(base_directory / 'ignore_file', 'a').close()
    open(base_directory / 'ignore_file', 'a').close()
    Path(base_directory / "symlink_file").symlink_to(base_directory /
                                                     "random.py")
    Path(base_directory / "symlink_dir").symlink_to(base_directory /
                                                    "ignore_dir")

    return base_directory
