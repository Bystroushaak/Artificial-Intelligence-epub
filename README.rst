About
=====
Scripts included in this project will allow you to create `epub <http://en.wikipedia.org/wiki/EPUB>`_ version of the `Artificial
Intelligence - foundations of computational agents <http://www.cs.ubc.ca/~poole/aibook/html/ArtInt.html>`_ website.

Requirements
------------
This script was tested under `Linux Mint <http://www.linuxmint.com/>`_ 17, which is based on Ubuntu 14.04.

To run this script, you will need to install ``calibre`` package from you repositories. It will also require ``pydhtmlparser`` and ``httpkie`` python packages, which can be installed using ``pip`` command.

To install all required packages, run::

    sudo apt-get install calibre python-pip

and::

   sudo pip install pydhtmlparser httpkie

You can also run the ``create_book.sh`` script and install all packages interactively.

How to
------
To create the `epub` file, open project directory in your terminal and run::

    ./create_book.sh

This command will download all informations from book's website and create `epub` version. This may take a while, depending on speed of your internet connection.

Note
----
This repository doesn't contain any content published at the book's website. Book is published under `Creative Commons Attribution-Noncommercial-No Derivative Works 2.5 Canada License <http://creativecommons.org/licenses/by-nc-nd/2.5/ca/>`_, which allows you to *"Share — copy and redistribute the material in any medium or format"*, which is exactly what this convertor does.