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
./window.sh -M # maximize window
./window.sh -m # restore window
./window.sh -f # toggle fullscreen
./window.sh -s n # send active window to desktop number "n"
```
In order to use these scripts, you'll probably want to set
them to specific keybindings. Also, you should use the full
path to the files, or move/copy/symlink them to any folder in
your `PATH`.
