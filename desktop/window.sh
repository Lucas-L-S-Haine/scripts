#!/usr/bin/sh

while getopts ":lr" option;
  do
    case $option in
      l)
        xdotool getactivewindow windowmove 0 0
        xdotool getactivewindow windowsize 679 y
        wmctrl :ACTIVE: -b add,maximized_vert
        xdotool getactivewindow windowmove 2 32
      ;;
      r)
        xdotool getactivewindow windowmove 0 0
        xdotool getactivewindow windowsize 679 y
        wmctrl :ACTIVE: -b add,maximized_vert
        xdotool getactivewindow windowmove 685 32
      ;;
      *)
        exit 1
      ;;
    esac
  done
