#!/usr/bin/env python
import os
import sys
import csv


HOME = os.environ["HOME"]
STEAM_GAMES_CSV = f"{HOME}/Documents/steam_games.csv"
ERROR_MESSAGE = f"""File {STEAM_GAMES_CSV} not found.
Please ensure the file is on the correct location and has the correct data.
"""


try:
    file_exists = False
    game_list_file = open(STEAM_GAMES_CSV, mode="r", encoding="utf-8")
    file_exists = True

    reader = csv.DictReader(game_list_file)
    games = [row for row in reader]
    print(games)
except:
    print(ERROR_MESSAGE, file=sys.stderr)
finally:
    if file_exists:
        game_list_file.close()


def newlines(text_list):
    for index in range(len(text_list)):
        text_list[index] += "\n"

    return text_list
