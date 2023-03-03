#!/usr/bin/env python
import sys

import yaml


def read_input():
    if sys.stdin.isatty():
        sys.exit(1)
    else:
        return sys.stdin.read().strip()


def parse(yaml_string):
    return yaml.safe_load(yaml_string)


def write_yaml():
    pass


def main():
    print(parse(read_input()))


if __name__ == "__main__":
    sys.exit(main())
