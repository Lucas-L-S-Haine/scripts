#!/usr/bin/env python
import os
import sys
import tempfile
from subprocess import run


try:
    exit_status = 0
    tmp_file = tempfile.NamedTemporaryFile(mode="w", delete=False).file

    if not sys.stdin.isatty():
        with open(tmp_file.name, mode="w") as file:
            file.write(sys.stdin.read())

    file = open(tmp_file.name, mode="r")

    if not sys.stderr.isatty():
        raise RuntimeError("Error: this script doesn't allow stderr redirection")

    run(["nvim", file.name], stdout=sys.stderr)

    sys.stdout.write(file.read())

except BaseException as error:
    print(error)
    exit_status = 1

finally:
    file.close()
    os.remove(tmp_file.name)
    sys.exit(exit_status)
