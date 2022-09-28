#!/usr/bin/env python
import requests
import subprocess
import json

try:
    url = "http://worldclockapi.com/api/json/utc/now"
    response = requests.get(url)
except:
    subprocess.run(["notify-send", "-t", "5000", "Error in update_clock.py"])

data = json.loads(response.text)

date, time = data["currentDateTime"].replace("Z", "").split("T")
hours, minutes = time.split(":")
hours = str(int(hours) - 3)
time = ":".join([hours, minutes])
datetime = " ".join([date, time])

command = ["doas", "timedatectl", "set-time", datetime]
subprocess.run(command)
