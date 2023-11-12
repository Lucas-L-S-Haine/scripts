import os
import sys
import csv
import subprocess as sp


PROG_TEMPLATE = """#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc > 1)
        return argc;

    char *steam_dir = "%s";
    char program[sizeof(steam_dir) + 18];
    char *command = "steam://rungameid/%s";

    if (isatty(1)) {
        snprintf(program, sizeof(program), "%%s/steam.sh", steam_dir);
    } else {
        snprintf(program, sizeof(program), "%%s/ubuntu12_32/steam", steam_dir);
    }

    char *args[] = {argv[0], command, NULL};

    execv(program, args);
    execvp("steam", args);
    return -1;
}
"""

HOME = os.environ["HOME"]
PATH = os.environ["PATH"]
XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME", f"{HOME}/.config")
XDG_DATA_HOME = os.environ.get("XDG_DATA_HOME", f"{HOME}/.local/share")
STEAM_GAMES_CSV = f"{XDG_CONFIG_HOME}/steam_games.csv"
GAMES_DIR = f"{HOME}/.games"

ERROR_MESSAGE = f"""file {STEAM_GAMES_CSV} not found.
Please ensure the file is on the correct location and has the correct data.
"""
TARGET_DIR_NOT_IN_PATH = f"target directory {GAMES_DIR} is not in $PATH"


def get_game_list() -> list[dict[str, str]]:
    """Read CSV data on games and return data as a list of dictionaries."""
    try:
        file_exists = False
        game_list_file = open(STEAM_GAMES_CSV, newline="", encoding="utf-8")
        file_exists = True

        csv_reader = csv.DictReader(game_list_file, dialect="unix")
        games = [entry for entry in csv_reader]
    except FileNotFoundError:
        print(f"Error: {ERROR_MESSAGE}", file=sys.stderr)
        sys.exit(3)
    finally:
        if file_exists:
            game_list_file.close()

    return games


def games_dir_is_in_path():
    """Validate whether games directory is in user's PATH."""
    try:
        path_list = PATH.split(":")
        path_list.index(GAMES_DIR)
    except ValueError:
        print(f"Error: {TARGET_DIR_NOT_IN_PATH}", file=sys.stderr)
        sys.exit(2)


def generate(game: dict[str, str], steam_dir: str) -> bytes:
    """Generate program to be compiled from a template."""
    return bytes(PROG_TEMPLATE % (steam_dir, game["gameid"]), encoding="utf-8")


def compile_game(game: dict[str, str]):
    """Compile a new program to launch the specified game."""
    name = game["name"]
    gameid = game["gameid"]
    output_file = f"{GAMES_DIR}/{name}"
    steam_dir = f"{XDG_DATA_HOME}/Steam"

    command = ["cc", "-o", output_file, "-x", "c", "-"]
    program = generate(game, steam_dir)

    sp.run(command, input=program)


def delete_game(game: dict[str, str]):
    """Delete compiled game launcher."""
    name = game["name"]
    file_name = f"{GAMES_DIR}/{name}"
    try:
        os.unlink(file_name)
    except FileNotFoundError:
        pass


def main():
    """Gets list of games from csv file and creates an executable script for
    each one of them"""
    games_dir_is_in_path()

    should_delete = False
    if len(sys.argv) > 1 and sys.argv[1] in ["delete", "remove", "unlink"]:
        should_delete = True

    games = get_game_list()

    if not should_delete:
        for game in games:
            filename = f"{GAMES_DIR}/{game['name']}"
            if not os.access(filename, os.F_OK):
                compile_game(game)
                print("New executable created at: %s" % (filename))
    else:
        for game in games:
            filename = f"{GAMES_DIR}/{game['name']}"
            if os.access(filename, os.F_OK):
                delete_game(game)
                print("Deleted executable: %s" % (filename))


if __name__ == "__main__":
    main()
