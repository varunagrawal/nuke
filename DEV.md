# Developer Documentation

This document summarizes the processes followed when developing and contributing to `nuke`. If you wish to submit a PR to fix an issue or add a feature, please read this document first.

## Test Driven Development

`nuke` follows Test Driven Development very stringently in order to ensure correct functionality. What this means is that before writing any functionality code, one is expected to write a test for it.

The tests go in the `tests` directory which contains python files with test code. The regular source code goes into the `nuke` directory. Any PR submitted will be required to have corresponding tests added as well, else the PR will be rejected without further review.

## Dependencies

The following dependencies are required to develop for `nuke`. They can be installed together using `uv`

```shell
uv sync
uv tool install tox --with tox-uv
```

- click
- rich
- colorama
- tox

## Running Tests

We use `poe` as a convenient action runner to ease various repetitive tasks.

To run tests, we can use
```shell
uv run poe test
```

For multiple python versions, `tox` is currently set up to read the tests from the `tests` directory and as such, we can as `poe` to run the tests.

```shell
# runs all the tests against supported Python versions
uv run poe tox
```

## Publishing

We can once again use `poe` to help with publishing:
```shell
uv run poe publish
```
