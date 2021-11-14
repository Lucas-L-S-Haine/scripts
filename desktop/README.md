These scripts’ purpose is to help you navigate your workspaces
regardless of `desktop environment` or `window manager`.

They require `xdotool` and `wmctrl` in order to work.
If you don't have these packages, you can install them using
your distro’s package manager.

## Installation:

### Debian
```
sudo apt-get install wmctrl xdotool
```
### Arch Linux
```
sudo pacman -S wmctrl xdotool
```

## Usage:
```
./desktop.sh -p # move to previous workspace
./desktop.sh -n # move to next workspace
./window.sh -l # tile window to left side of the screen
./window.sh -r # tile window to right side of the screen
```
If you want to set these scripts to specific keybindings, you'll
probably want to move/copy/symlink them to a folder in your `PATH`
or use your `DE`/`WM` to create custom commands, and type the complete
path to the files.
