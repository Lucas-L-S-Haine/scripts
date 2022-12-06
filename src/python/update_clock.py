#!/usr/bin/env python
import sys
import time
from subprocess import run
from requests import request
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


def main():

    try:
        datetime = request("head", "https://www.google.com").headers["date"]

        localtime = parse(datetime) + relativedelta(hours=-3)
        time_str = f"{localtime.date()} {localtime.time()}"

        run(["doas", "-n", "timedatectl", "set-ntp", "false"])
        time.sleep(1)
        run(["doas", "-n", "timedatectl", "set-time", time_str])
        time.sleep(1)
        run(["doas", "-n", "timedatectl", "set-ntp", "true"])
    except BaseException as error:
        summary = "Error: failed to update clock"
        body = error.__str__()

        run(["notify-send", "--expire-time=10000", summary, body])
    sys.exit(1)


if __name__ == "__main__":
    main()
