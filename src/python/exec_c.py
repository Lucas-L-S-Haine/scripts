#!/usr/bin/env python3
"""exec-c - Compile and execute C code

Usage:
    exec-c (-h | --help)
    exec-c <src_file> [<args>]...

Options:
    -h, --help  show this help message

Arguments:
    src_file    source code written in C
    args        command-line arguments
"""
import os
import sys
import subprocess as sp
import tempfile as tmp

from docopt import docopt


CC = "gcc"
CFLAGS = ["-Wall", "-Wextra", "-Werror"]

options = docopt(__doc__)

src_file = options["<src_file>"]
argv = options["<args>"]


def main():
    if src_file is None:
        print("Error: no file provided", file=sys.stderr)
        sys.exit(5)


    file = tmp.NamedTemporaryFile().name
    status = 0
    try:
        proc = sp.run([CC, *CFLAGS, "--output", file, src_file])
        status = proc.returncode
        if status == 0:
            proc = sp.run([file, *argv])
            status = proc.returncode
    finally:
        if os.access(file, os.F_OK):
            os.unlink(file)

        return status


if __name__ == "__main__":
    sys.exit(main())
