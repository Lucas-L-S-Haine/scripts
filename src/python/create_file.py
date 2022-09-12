#!/usr/bin/env python
import os
import sys
import csv


HOME = os.environ["HOME"]
PATH = os.environ["PATH"]
STEAM_GAMES_CSV = f"{HOME}/Documents/steam_games.csv"
ERROR_MESSAGE = f"""file {STEAM_GAMES_CSV} not found.
Please ensure the file is on the correct location and has the correct data.
"""
GAMES_DIR = f"{HOME}/.games"
TARGET_DIR_NOT_IN_PATH = f"target directory {GAMES_DIR} is not in $PATH"


try:
    path_list = PATH.split(":")
    path_list.index(GAMES_DIR)
except:
    print(f"Error: {TARGET_DIR_NOT_IN_PATH}", file=sys.stderr)
    sys.exit(2)


try:
    file_exists = False
    game_list_file = open(STEAM_GAMES_CSV, mode="r", encoding="utf-8")
    file_exists = True

    reader = csv.DictReader(game_list_file)
    games = [row for row in reader]
except:
    print(f"Error: {ERROR_MESSAGE}", file=sys.stderr)
finally:
    if file_exists:
        game_list_file.close()


def newlines(text_list):
    for index in range(len(text_list)):
        text_list[index] += "\n"

    return text_list
