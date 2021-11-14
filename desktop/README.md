This script’s purpose is to help you navigate your workspaces
regardless of desktop environment or window manager.

It requires `xdotool` and `wmctrl` in order to work.
If you don't have these packages, you can install them using
your distro’s package manager.

## Debian:
```
sudo apt-get install wmctrl xdotool
```
## Arch Linux:
```
sudo pacman -S wmctrl xdotool
```

## Usage:
```
./desktop -p # move to previous workspace
./desktop -n # move to next workspace
```
