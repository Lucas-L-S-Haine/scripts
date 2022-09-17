#!/usr/bin/env python
import requests
import subprocess
import json

url = "http://worldtimeapi.org/api/timezone/America/Sao_Paulo"
response = requests.get(url)

datetime = json.loads(response.text)["datetime"]
datetime = datetime.replace("T", " ").split(".")[0]

command = ["timedatectl", "set-time", datetime]
subprocess.run(command)
