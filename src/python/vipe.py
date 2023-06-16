#!/usr/bin/env python
import os
import sys
import tempfile
from subprocess import run, check_output


TTY_NAME = "/dev/tty"


def get_editor():
    """Get editor name by reading environment variables VISUAL and EDITOR """

    EDITOR = os.environ.get("EDITOR", "vi")
    VISUAL = os.environ.get("VISUAL", EDITOR)

    if VISUAL.find("emacs") != -1:
        return f"emacsclient --create-frame --alternate-editor={EDITOR}"

    return VISUAL


def main():
    """Reads input from stdin, edits on EDITOR and pipes into stdout"""

    try:
        input_tty = open(TTY_NAME, mode="r")
        output_tty = open(TTY_NAME, mode="w")
        tmp_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        editor = get_editor()

        if not sys.stdin.isatty():
            with open(tmp_file.name, mode="w") as file:
                file.write(sys.stdin.read())

        file = open(tmp_file.name, mode="r")

        run([*editor.split(), file.name], stdin=input_tty, stdout=output_tty)

        sys.stdout.write(file.read())

    finally:
        file.close()
        input_tty.close()
        output_tty.close()

        os.remove(tmp_file.name)


if __name__ == "__main__":
    main()
