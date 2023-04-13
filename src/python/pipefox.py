#!/usr/bin/env python3
"""Pipefox - A simple script to pipe html into your browser

Usage:
    pipefox.py [--help | -h]
    pipefox.py [--format=<format> | -f <format>]
               [--browser=<browser> | -b <browser>] [<file> | -]

Positional Arguments:
    file                     The file from which the html content will be read.
                             If <file> is "-", then pipefox.py will read from
                             stdin.

Options:
    -h, --help               show this help message and exit
    -f, --format=<format>    the format to use for the file
    -b, --browser=<browser>  The browser to open the html page
"""
import os
import sys
import tempfile as tmp
import subprocess as sp
import io

from docopt import docopt


options = docopt(__doc__)

file_name = options["<file>"]
browser = options["--browser"] or os.environ.get("BROWSER", "x-www-browser")


should_read_from_tty = file_name == "-" or file_name is None


extension = options["--format"]
use_file_extension = not should_read_from_tty and len(file_name.split(".")) > 1

if file_name[0] == ".":
    use_file_extension = False

if extension is None and use_file_extension:
    extension = file_name.split(".")[-1]
elif extension is None:
    extension = "html"


file = io.TextIOBase()
try:
    if should_read_from_tty:
        file = sys.stdin
    else:
        file = open(options["<file>"], mode="r")

    with tmp.NamedTemporaryFile(suffix=f".{extension}") as tmp_file:
        tmp_file.write(file.read().encode())

        sp.run([browser, tmp_file.name], input=tmp_file.read())

finally:
    file.close()
