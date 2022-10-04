#!/usr/bin/env python
import sys
import time
from subprocess import run
from requests import request
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

try:
    datetime = request("head", "http://www.google.com").headers["date"]
except BaseException as Error:
    run(["notify-send", "--expire-time=5000", "Error: failed to update clock"])
    run(["notify-send", "--expire-time=5000", Error.__str__()])
    sys.exit(1)

localtime = parse(datetime) + relativedelta(hours=-3)
time_str = f"{localtime.date()} {localtime.time()}"

run(["doas", "timedatectl", "set-ntp", "false"])
time.sleep(1)
run(["doas", "timedatectl", "set-time", time_str])
time.sleep(1)
run(["doas", "timedatectl", "set-ntp", "true"])
