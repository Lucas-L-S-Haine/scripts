import sys
import os
import stat
from getopt import GetoptError, gnu_getopt as getopt

from triade.lib import write


SHORT_OPTS = "a"
LONG_OPTS = ["all"]


def parse_opts():
    return getopt(sys.argv[1:], SHORT_OPTS, LONG_OPTS)


def ok():
    if sys.stdout.isatty():
        print("\x1b[1;32m", "ok", "\x1b[0m", sep="")
    else:
        print("ok")


def fail():
    if sys.stdout.isatty():
        print("\x1b[1;31m", "fail", "\x1b[0m", sep="")
    else:
        print("fail")


def log(*args):
    print(*args, end=" ")


def read_file(filename=".", filter_callback=None):
    """Takes the name of a file as argument and return data on it. If the file
    is a directory, open the directory and return information on all its files.
    Otherwise, just return information on the single file."""
    stats = os.stat(filename, follow_symlinks=False)

    if stat.S_IFMT(stats.st_mode) == stat.S_IFDIR:
        files = []
        with os.scandir(filename) as it:
            entries = filter(filter_callback, it)
            for entry in entries:
                name = entry.name
                filetype = get_file_type(os.path.join(filename, entry.name))
                tag_name = "dir" if filetype == "directory" else "file"
                files.append({
                    "tag_name": tag_name,
                    "attributes": {"name": name, "type": filetype}
                })

        return {
            "tag_name": "dir",
            "attributes": {"name": filename, "type": "directory"},
            "child_nodes": files
        }

    else:
        filetype = get_file_type(filename)

        return {
            "tag_name": "file",
            "attributes": {"name": filename, "type": filetype}
        }


def get_file_type(filename):
    stats = os.stat(filename, follow_symlinks=False)

    match stat.S_IFMT(stats.st_mode):
        case stat.S_IFREG:
            return "regularFile"
        case stat.S_IFDIR:
            return "directory"
        case stat.S_IFLNK:
            return "symbolicLink"
        case stat.S_IFIFO:
            return "FIFO"
        case stat.S_IFSOCK:
            return "socket"
        case stat.S_IFBLK:
            return "blockDevice"
        case stat.S_IFCHR:
            return "characterDevice"
        case stat.S_IFDOOR:
            return "door"
        case stat.S_IFPORT:
            return "eventPort"
        case stat.S_IFWHT:
            return "whiteout"
        case _:
            return "???"


def main():
    get_all = False
    opts, args = parse_opts()
    for flag, _ in opts:
        if flag in ["-a", "--all"]:
            get_all = True

    file = args[0] if len(args) > 0 else "."
    callback = (lambda e: not e.name.startswith(".")) if not get_all else None

    output = write(read_file(file, callback), "xml")
    print(output)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as err:
        fail()
        raise err
