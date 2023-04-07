#!/usr/bin/env python
import sys
import time
from subprocess import run

from requests import request
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


def notify(summary: str, body: str):
    if sys.stderr.isatty():
        print(summary, file=sys.stderr)
        print(body, file=sys.stderr)
    else:
        run(["notify-send", "--expire-time=10000", summary, body])


def get_time():
    try:
        time_str = sys.argv[1]
    except IndexError:
        datetime = request("head", "https://www.google.com").headers["date"]

        localtime = parse(datetime) + relativedelta(hours=-3)
        time_str = f"{localtime.date()} {localtime.time()}"

    return time_str


def main():
    """Fetches time from Google and updates system clock"""

    try:
        time_str = get_time()

        run(["doas", "-n", "timedatectl", "set-ntp", "false"])
        time.sleep(1)
        run(["doas", "-n", "timedatectl", "set-time", time_str])
        time.sleep(1)
        run(["doas", "-n", "timedatectl", "set-ntp", "true"])
    except Exception as error:
        summary = "Error: failed to update clock"
        body = str(error)

        notify(summary, body)
        sys.exit(1)


if __name__ == "__main__":
    main()
