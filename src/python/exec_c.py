"""Compile one or more C source code files into a temporary binary file and
execute it immediately.

The script uses its own options to choose the compiler, the compiler flags and
the linking flags, along with source code files. If you want to pass arguments
directly to the compiled program, you can do so by passing "--" to the
commandline, followed by the desired arguments.
"""
import os
import sys
import subprocess as sp
import tempfile as tmp
from getopt import GetoptError, gnu_getopt as getopt


SHORT_OPTS = "hc:f:l:n"
LONG_OPTS  = ["help", "cc=", "cflags=", "ldflags=", "compiler=", "flags=",
              "dry-run"]


CC      = os.environ.get("CC", "cc")
CFLAGS  = os.environ.get("CFLAGS", "-Wall:-Werror:-Wextra")
LDFLAGS = os.environ.get("LDFLAGS", "")


def separate_arguments(argv):
    """Separate list in two by searching for a "--" argument."""
    try:
        index = argv.index("--")
        return argv[:index], argv[index + 1:]
    except ValueError:
        return argv, []


def print_help():
    """Print help message."""
    message = f"""Usage:
    {os.path.basename(sys.argv[0])} (-h | --help)
    {os.path.basename(sys.argv[0])} [-c <compiler> | --cc=<compiler> | --compiler=<compiler>]
           [-f <flags> | --flags=<flags>]... <src_file>... [--] [<arg>]...

Options:
    -h, --help               show this help message
    -c, --cc=<compiler>      choose a different compiler [default: cc]
    -f, --cflags=<flags>     specify the compiler flags [default: -Wall -Wextra -Werror]
    -l, --ldflags=<flags>    specify linking flags

Arguments:
    src_file    source code written in C
    arg         command-line arguments"""
    print(message)
    sys.exit(0)


def dry_run(options, files, arguments):
    """Simulate the program's execution."""
    compiler = options["compiler"]
    cflags   = options["cflags"]
    ldflags  = options["ldflags"]

    output_file = tmp.NamedTemporaryFile().name

    compile_program = [compiler, *cflags, "-o", output_file, *files]
    execute_program = [output_file, *arguments]
    print(*get_truthy_values(compile_program))
    print(*get_truthy_values(execute_program))
    sys.exit(0)


def get_compiler_options(option_list, **kwargs):
    """Organize compiler options in a dictionary."""
    options = kwargs
    options["dry-run"] = False

    for flag, value in option_list:
        if flag in ["-h", "--help"]:
            print_help()
        elif flag in ["-c", "--cc", "--compiler"]:
            options["compiler"] = value
        elif flag in ["-f", "--cflags", "--flags"]:
            options["cflags"] = value.split()
        elif flag in ["-l", "--ldflags"]:
            options["ldflags"] = value.split()
        elif flag in ["-n", "--dry-run"]:
            options["dry-run"] = True

    return options


def parse_commandline_arguments(argv=sys.argv[1:]):
    """Parse all options and arguments necessary for the program's execution."""
    compiler_args, arguments = separate_arguments(argv)

    try:
        options, files = getopt(compiler_args, SHORT_OPTS, LONG_OPTS)
    except GetoptError as e:
        print("Error:", e.msg, file=sys.stderr)
        sys.exit(2)

    options = get_compiler_options(
        options, compiler=CC, cflags=CFLAGS.split(":"),
        ldflags=LDFLAGS.split(":")
    )

    return options, files, arguments


def get_truthy_values(value_list):
    """Return a copy of a list containing only truthy values."""
    values = []
    for value in value_list:
        if value:
            values.append(value)

    return values


def main():
    options, files, arguments = parse_commandline_arguments()

    compiler = options["compiler"]
    cflags   = options["cflags"]
    ldflags  = options["ldflags"]

    if options["dry-run"]:
        dry_run(options, files, arguments)

    if not files:
        print("Error: no filename was provided", file=sys.stderr)
        return 5

    status = 1
    try:
        output_file = tmp.NamedTemporaryFile().name
        command = [compiler, *cflags, "-o", output_file, *files, *ldflags]
        command = get_truthy_values(command)
        proc = sp.run(command)
        status = proc.returncode
        if status == 0:
            command = get_truthy_values([output_file, *arguments])
            proc = sp.run(command)
            status = proc.returncode
    except Exception as e:
        print("Error:", e.args[0], file=sys.stderr)
        status = 1
    finally:
        if os.access(output_file, os.F_OK):
            os.unlink(output_file)

        return status


if __name__ == "__main__":
    sys.exit(main())
