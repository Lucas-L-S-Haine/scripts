import os
import os.path
import re
import tarfile
import tempfile
import shutil
import json
import sys

from bumpline.version import Version


HOME = os.environ["HOME"]
TARGET_DIR = f"{HOME}/Downloads/tar"
DISCORD_RE = re.compile(r"discord.+tar\.gz")


def is_discord_tarball(filename: str) -> bool:
    return DISCORD_RE.match(filename)


def get_discord_version(discord_dir):
    if not os.path.exists(discord_dir):
        return Version("0")

    file = os.path.join(discord_dir, "resources/build_info.json")

    with open(file, mode="r") as build_info:
        version = Version(json.load(build_info)["version"])

    return version


def get_version_from_name(filename):
    match = re.search(r"-(\d+\.\d+\.\d+)", filename)

    if match:
        version_number = match.group(1)
        return Version(version_number)
    else:
        return Version("0")


def main():
    os.chdir(TARGET_DIR)

    all_files = os.listdir()
    discord_files = list(filter(is_discord_tarball, all_files))
    discord_files.sort(reverse=True)

    newest_file = discord_files[0]

    current_version = get_discord_version("Discord")
    newest_file_version = get_version_from_name(newest_file)

    if not os.path.exists(f"{HOME}/.local/bin/discord"):
        discord_bin = os.path.join(TARGET_DIR, "Discord/Discord")
        destination = f"{HOME}/.local/bin/discord"
        os.symlink(discord_bin, destination)
        print("Symbolic link created at: {destination}")

    if current_version >= newest_file_version:
        print("Discord is already in its newest version.")
        return 0

    os.rename("Discord", "OldDiscord")

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(newest_file, mode="r:gz") as tarball:
            try:
                tarball.extractall()
                shutil.move("OldDiscord", tmpdir)
            except tarfile.ExtractError:
                os.rename("OldDiscord", "Discord")
                print("Error: cannot extract files from tarball",
                      file=sys.stderr)
                return 1

    print("Discord updated from version %s to version %s" %
          (current_version, newest_file_version))

    return 0


if __name__ == "__main__":
    sys.exit(main())
