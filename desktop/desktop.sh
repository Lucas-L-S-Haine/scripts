#!/usr/bin/sh

while getopts ":np" option;
  do
    case $option in
      n)
        xdotool set_desktop --relative -- +1
      ;;
      p)
        xdotool set_desktop --relative -- -1
      ;;
      *)
        exit 1
      ;;
    esac
  done
