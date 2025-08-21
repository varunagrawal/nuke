"""Unit tests for the utils.py module."""

import crayons

from nuke import utils


def test_fg():
    """Test the foreground color generator function."""
    text = "│   "
    color = 241
    color_str = utils.fg("│   ", 241)

    assert color_str == f"\33[38;5;{color}m{text}\33[0m"


def test_bg():
    """Test the foreground color generator function."""
    text = "│   "
    color = 241
    color_str = utils.bg("│   ", 241)

    assert color_str == f"\33[48;5;{color}m{text}\33[0m"


def test_get_colorized(directory):
    """Test colorization of various filesystem components."""
    # Directory
    s: crayons.ColoredString = utils.get_colorized(directory)
    assert s.color == "BLUE"

    # File
    s: crayons.ColoredString = utils.get_colorized(directory / "random.py")
    assert s.color == "GREEN"

    # Mount point

    # Symlink
    s: crayons.ColoredString = utils.get_colorized(directory / "symlink_file")
    assert s.color == "CYAN"

    # Socket

    # Other


def test_parse_ignore_file(directory):
    """Test the `parse_ignore_file` function."""

    ignore_file = directory / "nukeignore"

    with open(ignore_file, "w+", encoding="UTF-8") as f:
        f.write("sample.py\n")
        f.write("# This is a comment\n")
        f.write("another.txt\n")
        f.write("with_ending_space.txt   \n")
        f.write("ignore_dir/\n")

    ignore_list = utils.parse_ignore_file(ignore_file.resolve(), directory)

    expected_ignore_list = [
        'test_directory/sample.py', 'test_directory/another.txt',
        'test_directory/with_ending_space.txt', 'test_directory/ignore_dir',
        'test_directory/ignore_dir/*'
    ]

    assert ignore_list == expected_ignore_list
