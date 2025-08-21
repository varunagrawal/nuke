"""Unit tests for the CLI entry point."""

import sys

from click.testing import CliRunner

from nuke.cli import main


def test_invoke_cli(directory):
    """Test which simulates calling `nuke` from the command line."""
    runner = CliRunner()
    result = runner.invoke(main, [str(directory), "-y"])
    assert result.exit_code == 0


def test_with_missing_directory():
    """Test which simulates calling `nuke` from the command line."""
    runner = CliRunner()
    result = runner.invoke(main, ["directory_which_doesnt_exist", "-y"])
    assert result.exit_code == 0


def test_list_files(directory):
    """Test listing of files to delete."""
    runner = CliRunner()
    result = runner.invoke(main, [str(directory), "-l", "-y"])

    assert result.exit_code == 0

    if sys.platform == "linux":
        expected_output = """├── ignore_dir/
test_directory/
├── symlink_file
├── ignore_file
├── another.py
├── symlink_dir
└── random.py
"""

    elif sys.platform == "darwin":  # MacOS
        expected_output = """├── ignore_dir/
test_directory/
├── symlink_dir
├── ignore_file
├── random.py
├── another.py
└── symlink_file
"""
    else:  # Something else (throw error)
        expected_output = ""

    assert result.output == expected_output
    assert result.output == expected_output
    assert result.output == expected_output
