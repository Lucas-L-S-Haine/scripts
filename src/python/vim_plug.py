import sys
import os
from getopt import getopt, GetoptError

from requests import request, ConnectionError, HTTPError, Timeout


BASE_URL = "https://raw.githubusercontent.com/junegunn/vim-plug/"
SHORT_OPTS = "hvno:"
LONG_OPTS = ["help", "vim", "nvim", "output="]
HOME = os.environ["HOME"]
XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME", f"{HOME}/.config")


def print_help(name):
    """Print help message."""
    message = """Usage:
    %s (-h | --help)
    %s [-v | --vim] [-n | --nvim]
    %s -o <output_file>""" % (name, name, name)

    print(message)
    sys.exit(0)


def parse_commandline_arguments(args=sys.argv[1:]):
    """Parse options given on the command line."""
    options = {"vim": False, "nvim": False}

    try:
        opts, _ = getopt(args, SHORT_OPTS, LONG_OPTS)
    except GetoptError as e:
        print("Error:", e.msg, file=sys.stderr)
        sys.exit(2)

    for flag, value in opts:
        if flag in ["-h", "--help"]:
            print_help(os.path.basename(sys.argv[0]))
        elif flag in ["-v", "--vim"]:
            options["vim"] = True
        elif flag in ["-n", "--nvim"]:
            options["nvim"] = True
        elif flag in ["-o", "--output"]:
            options["output"] = value

    if "output" in options and (options["vim"] or options["nvim"]):
        print("Error: can't pass -o along with either -v or -n",
              file=sys.stderr)
        sys.exit(3)

    return options


def write_file(response, options):
    """Write response text to output file."""
    if options["vim"]:
        os.makedirs(f"{HOME}/.vim/autoload", exist_ok=True)
        vim_plug = f"{HOME}/.vim/autoload/plug.vim"
        with open(vim_plug, "w") as file:
            file.write(response)
        print(f"vim-plug written to {HOME}/.vim/autoload/plug.vim")

    if options["nvim"]:
        os.makedirs(f"{XDG_CONFIG_HOME}/nvim/autoload", exist_ok=True)
        vim_plug = f"{XDG_CONFIG_HOME}/nvim/autoload/plug.vim"
        with open(vim_plug, "w") as file:
            file.write(response)
        print(f"vim-plug written to {XDG_CONFIG_HOME}/nvim/autoload/plug.vim")

    if "output" in options:
        output_dir = os.path.dirname(options["output"])
        output_file = options["output"]
        os.makedirs(output_dir, exist_ok=True)
        with open(output_file, "w") as file:
            file.write(response)
        print(f"vim-plug written to {output_file}")


def main():
    options = parse_commandline_arguments()

    try:
        response = request("GET", "%s/master/plug.vim" % (BASE_URL),
                           allow_redirects=True, timeout=4)
        write_file(response.text, options)
    except FileExistsError as e:
        print("Error: file %s already exists" % e.filename, file=sys.stderr)

        return e.errno
    except (ConnectionError, HTTPError, Timeout) as e:
        print("Error:", e, file=sys.stderr)

        return e.errno


if __name__ == "__main__":
    sys.exit(main())
