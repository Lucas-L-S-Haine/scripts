#!/usr/bin/env python3
import os
import sys
import tempfile
import subprocess as sp


TTY_NAME = "/dev/tty"

is_emacs = lambda editor: editor.find("emacs") != -1


def get_editor():
    """Get editor name by reading environment variables VISUAL and EDITOR """

    EDITOR = os.environ.get("EDITOR", "vi")
    VISUAL = os.environ.get("VISUAL", EDITOR)

    if is_emacs(VISUAL) and not is_emacs(EDITOR):
        ALT_EDITOR = os.environ.get("ALTERNATE_EDITOR", EDITOR)
        VISUAL = f"emacsclient --create-frame --alternate-editor={ALT_EDITOR}"
    elif is_emacs(VISUAL):
        ALT_EDITOR = os.environ.get("ALTERNATE_EDITOR", "vi")
        VISUAL = f"emacsclient --create-frame --alternate-editor={ALT_EDITOR}"

    return VISUAL


def edit_file(editor, file, stdin, stdout):
    if is_emacs(editor):
        sp.run([*editor.split(), file.name], stdin=sp.DEVNULL, stdout=sp.DEVNULL)
    else:
        sp.run([*editor.split(), file.name], stdin=stdin, stdout=stdout)


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

        edit_file(editor, file, input_tty, output_tty)

        sys.stdout.write(file.read())

    finally:
        file.close()
        input_tty.close()
        output_tty.close()

        os.remove(tmp_file.name)


if __name__ == "__main__":
    main()
