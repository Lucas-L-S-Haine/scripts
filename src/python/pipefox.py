#!/usr/bin/env python3
import os
import sys
import tempfile as tmp
import subprocess as sp
import argparse


BROWSER = os.environ.get("BROWSER", "x-www-browser")


parser = argparse.ArgumentParser()
parser.add_argument("browser", nargs="?", default=BROWSER)

args = parser.parse_args()


with tmp.NamedTemporaryFile(suffix=".html") as tmp_file:
    tmp_file.write(sys.stdin.read().encode())

    sp.run([args.browser, tmp_file.name], input=tmp_file.read())
