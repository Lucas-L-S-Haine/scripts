#!/usr/bin/env python3
"""exec-c - Compile and execute C code

Usage:
    exec-c (-h | --help)
    exec-c [-c <compiler> | --cc=<compiler> | --compiler=<compiler>]
           [-f <flags> | --flags=<flags>]... <src_file> [<args>]...

Options:
    -h, --help              show this help message
    -c, --cc=<compiler>     choose a different compiler[default: gcc]
    --compiler=<compiler>   alias for --cc
    -f, --flags=<flags>     specify the compiler flags[default: -Wall -Wextra -Werror]

Arguments:
    src_file    source code written in C
    args        command-line arguments
"""
import os
import sys
import subprocess as sp
import tempfile as tmp

from docopt import docopt


options = docopt(__doc__)
if options["--compiler"] is None:
    options["--compiler"] = options["--cc"]
else:
    options["--cc"] = options["--compiler"]

CC = options["--compiler"]
CFLAGS = list(set(options["--flags"]))

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
