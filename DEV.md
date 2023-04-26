# Developer Documentation

This document summarizes the processes followed when developing and contributing to `nuke`. If you wish to submit a PR to fix an issue or add a feature, please read this document first.

## Test Driven Development

`nuke` follows Test Driven Development very stringently in order to ensure correct functionality. What this means is that before writing any functionality code, one is expected to write a test for it.

The tests go in the `tests` directory which contains python files with test code. The regular source code goes into the `nuke` directory. Any PR submitted will be required to have corresponding tests added as well, else the PR will be rejected without further review.

## Dependencies

The following dependencies are required to develop for `nuke`. They can be installed together using `poetry`

```shell
poetry install
```

- click
- rich
- colorama
- tox

## Running Tests

`tox` is currently set up to read the tests from the `tests` directory and as such, one only needs to run the `tox` command.

```shell
# runs all the tests against Python 3.7, 3.8, 3.9, 3.10 & 3.11
tox

# test only against Python 3.7
tox -e 37
```

## Makefile

There is also a `Makefile` set up to ease various repetitive tasks.

- Default: The default `make` command runs the `tox` tests.
- `make submit`: This packages and submits the latest version of the code to PyPI (only maintainer accessible).
