#!/usr/bin/env python3
"""Pipefox - A simple script to pipe html into your browser

Usage:
    pipefox.py [--help | -h]
    pipefox.py [--format=<format> | -f <format>] [<browser>] [<file> | -]

Positional Arguments:
    browser                The browser to open the html page
    file                   The file from which the html content will be read.
                           If <file> is "-", then pipefox.py will read from
                           stdin.

Options:
    -h, --help             show this help message and exit
    -f, --format=<format>  the format to use for the file [default: html]
"""
import os
import sys
import tempfile as tmp
import subprocess as sp
import io

from docopt import docopt


options = docopt(__doc__)

browser = options["<browser>"] or os.environ.get("BROWSER", "x-www-browser")
should_read_from_tty = options["<file>"] == "-" or options["<file>"] is None


file = io.TextIOBase()
try:
    if should_read_from_tty:
        file = sys.stdin
    else:
        file = open(options["<file>"], mode="r")

    with tmp.NamedTemporaryFile(suffix=".html") as tmp_file:
        tmp_file.write(file.read().encode())

        sp.run([browser, tmp_file.name], input=tmp_file.read())

finally:
    file.close()
