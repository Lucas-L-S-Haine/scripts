"""update_clock.py - This script updates the system clock

Usage:
    update_clock.py [-h | --help]
    update_clock.py [<datetime> | <date> <time>]

Options:
    -h, --help  show this help message and exit

Arguments:
    date        a string with date, formatted as YYYY-MM-DD
    time        a string with time, formatted as hh:mm:ss
    datetime    a string with date and time in ISO format
"""
import sys
import time
from subprocess import run

from requests import request
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from docopt import docopt


def notify(summary: str, body: str):
    "Send error messages through stderr or notify-send, if stderr is not a tty"

    if sys.stderr.isatty():
        print(summary, file=sys.stderr)
        print(body, file=sys.stderr)
    else:
        run(["notify-send", "--expire-time=10000", summary, body])


def get_time():
    "Get date and time string from argv or fetch from Google"

    options = docopt(__doc__)

    if len(sys.argv[1:]) == 0:
        with request("head", "https://www.google.com") as response:
            datetime = response.headers["date"]

            localtime = parse(datetime) + relativedelta(hours=-3)
            time_str = f"{localtime.date()} {localtime.time()}"
    elif len(sys.argv[1:]) == 1:
        time_str = options["<datetime>"]
    elif len(sys.argv[1:]) == 2:
        time_str = f"{options['<date>']} {options['<time>']}"

    return time_str


def main():
    "Call the get_time function and use it to update the system clock"

    try:
        time_str = get_time()

        run(["doas", "-n", "date", "--set", time_str])
    except Exception as error:
        summary = "Error: failed to update clock"
        body = str(error)

        notify(summary, body)
        sys.exit(1)


if __name__ == "__main__":
    main()
