"""Entry point for the CLI application."""

from pathlib import Path

import click
import crayons

from nuke.nuke import list_files_tree, nuke


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("directory", nargs=1, default=Path.cwd())
@click.option("-l",
              is_flag=True,
              default=False,
              help="List all the files that will be nuked")
@click.option("-y",
              is_flag=True,
              is_eager=True,
              default=False,
              help="Flag to confirm nuking")
def main(directory: str, l: bool, y: bool):  # noqa: E741
    """
    Nuke (aka delete the contents of) the DIRECTORY specified.
    Default directory is the current directory.
    """
    try:
        # expand and resolve the input directory path
        directory = Path(directory).expanduser().resolve(strict=True)
    except FileNotFoundError:
        click.secho(
            "Invalid directory specified. Please ensure directory is valid.",
            fg="red")

    if l:
        list_files_tree(directory=directory)
        return

    if y or click.confirm(
            "Are you sure you want to nuke directory " +
            crayons.blue(directory) + "?",
            default=True,  # sets the prompt to Y/n
            abort=False,
    ):
        nuke(directory)
