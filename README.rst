Nuke
=====

Command line tool nuking a directory.

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
    :target: https://saythanks.io/to/varunagrawal

Installation
------------

Installing ``nuke`` is intended to be super easy. The only dependency is a supported Python interpreter. You can get ``nuke`` via ``pip``:

.. code-block:: shell

    $ pip install nuke

``nuke`` is supported for Python versions 2.7, 3.5 & 3.6+.


Usage
-------

The most common usage of ``nuke`` is when you wish to recreate a build directory for a build program such as CMake.

To use ``nuke``, you just call :code:`nuke` from the command line and specify the directory you wish to nuke: 

.. code-block:: shell
    
    $ nuke path/to/directory

If you are already in the directory you wish to nuke, you don't need to exit the directory. Calling :code:`nuke` without any arguments will nuke the current directory:

.. code-block:: shell

    $ nuke  # same as "nuke ."

Since nuking is a dangerous operation and you don't want to inadvertently delete something important, `nuke` always asks you to confirm the nuking of a directory. If you wish to override this since you know what you are doing or you wish to use ``nuke`` in a shell script, you can pass in the ``-y`` flag:

.. code-block:: shell

    $ nuke -y /path/to/dir/
