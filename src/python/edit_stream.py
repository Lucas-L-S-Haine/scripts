#!/usr/bin/env python
import os
import sys
import tempfile
from subprocess import run


def main():
    """Reads input from stdin, edits on neovim and pipes into stdout"""

    ERROR_MESSAGE = "Error: this script doesn't allow stderr redirection"

    try:
        exit_status = 0
        tmp_file = tempfile.NamedTemporaryFile(mode="w", delete=False).file

        if not sys.stdin.isatty():
            with open(tmp_file.name, mode="w") as file:
                file.write(sys.stdin.read())

        file = open(tmp_file.name, mode="r")

        if not sys.stderr.isatty():
            raise RuntimeError(ERROR_MESSAGE)

        run(["nvim", file.name], stdout=sys.stderr)

        sys.stdout.write(file.read())

    except BaseException as error:
        print(error)
        exit_status = 1

    finally:
        file.close()
        os.remove(tmp_file.name)
        sys.exit(exit_status)


if __name__ == "__main__":
    main()
