#!/usr/bin/env python
import os
import sys
import tempfile
from subprocess import run


def main():
    """Reads input from stdin, edits on neovim and pipes into stdout"""

    try:
        input_tty = open("/dev/tty", mode="r")
        output_tty = open("/dev/tty", mode="w")
        tmp_file = tempfile.NamedTemporaryFile(mode="w", delete=False).file

        if not sys.stdin.isatty():
            with open(tmp_file.name, mode="w") as file:
                file.write(sys.stdin.read())

        file = open(tmp_file.name, mode="r")

        run(["nvim", file.name], stdin=input_tty, stdout=output_tty)

        sys.stdout.write(file.read())

    finally:
        file.close()
        os.remove(tmp_file.name)


if __name__ == "__main__":
    main()
