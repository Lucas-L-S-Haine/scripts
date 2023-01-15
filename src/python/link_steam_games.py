#!/usr/bin/env python
import os
import sys
import csv


HOME = os.environ["HOME"]
PATH = os.environ["PATH"]
STEAM_GAMES_CSV = f"{HOME}/Documents/steam_games.csv"
GAMES_DIR = f"{HOME}/.games"

ERROR_MESSAGE = f"""file {STEAM_GAMES_CSV} not found.
Please ensure the file is on the correct location and has the correct data.
"""
TARGET_DIR_NOT_IN_PATH = f"target directory {GAMES_DIR} is not in $PATH"


def newlines(text_list):
    for index in range(len(text_list)):
        text_list[index] += "\n"

    return text_list


def main():
    """Gets list of games from csv file and creates an executable script for
    each one of them"""


    try:
        path_list = PATH.split(":")
        path_list.index(GAMES_DIR)
    except ValueError:
        print(f"Error: {TARGET_DIR_NOT_IN_PATH}", file=sys.stderr)
        sys.exit(2)


    try:
        file_exists = False
        game_list_file = open(STEAM_GAMES_CSV, mode="r", encoding="utf-8")
        file_exists = True

        csv_reader = csv.DictReader(game_list_file)
        games = [row for row in csv_reader]
    except FileNotFoundError:
        print(f"Error: {ERROR_MESSAGE}", file=sys.stderr)
        sys.exit(3)
    finally:
        if file_exists:
            game_list_file.close()


    for game in games:
        gameid = game["gameid"]
        name = game["name"]
        file_name = f"{GAMES_DIR}/{name}"
        command = ["#!/bin/sh", "", f"exec steam steam://rungameid/{gameid}"]

        with open(file_name, mode="w", encoding="utf-8") as file:
            file.writelines(newlines(command))
            os.chmod(file.name, 0o755)


if __name__ == "__main__":
    main()
