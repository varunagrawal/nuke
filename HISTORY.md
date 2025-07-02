## Version History

#### 2.6.0

Switch to `uv` for package management.

#### 2.5.2

Clean up dependencies.

#### 2.5.1

Use `rich` for nicer progress bars.

#### 2.4.5

Fix bug with matching directories without trailing slash.

#### 2.4.4

- Change the main entry file.
- Add new modules to better organize code.
- Pretty printing of deletion tree.

#### 2.4.3

Switched from `pipenv` to the much nicer `poetry`.

#### 2.2.2

Use of `pipenv` as default toolchain.

#### 2.2.1

Fixed bug in the `-l` list functionality so that ignored files are not displayed.

#### 2.2.0

Major bugfix in the ``.nukeignore`` functionality. ``nuke`` now ignores whole directories if the pattern ends in a slash (``/``).
Also, ``-l`` prints out files as a directory tree.

#### 2.1.1

Updated Python Trove Classifiers.

#### 2.1.0

Migrated from ``clint`` to ``click`` to streamline code. Added ``-l`` flag to list files that will be deleted without deleting them.

#### 2.0.0

Added feature to ignore files to nuke based on a ``.nukeignore`` file on a per directory level.

#### 1.0.5

Minor bug fixes.

#### 1.0

Nuke is out!