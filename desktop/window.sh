#!/usr/bin/sh

while getopts ":lrMmf" option;
  do
    case $option in
      l)
        xdotool getactivewindow windowmove 0 0
        xdotool getactivewindow windowsize 679 y
        wmctrl -r :ACTIVE: -b add,maximized_vert
        xdotool getactivewindow windowmove 2 32
      ;;
      r)
        xdotool getactivewindow windowmove 0 0
        xdotool getactivewindow windowsize 679 y
        wmctrl -r :ACTIVE: -b add,maximized_vert
        xdotool getactivewindow windowmove 685 32
      ;;
      M)
        wmctrl -r :ACTIVE: -b add,maximized_vert
        wmctrl -r :ACTIVE: -b add,maximized_horz
      ;;
      m)
        wmctrl -r :ACTIVE: -b remove,maximized_vert
        wmctrl -r :ACTIVE: -b remove,maximized_horz
      ;;
      f)
        wmctrl -r :ACTIVE: -b toggle,fullscreen
      ;;
      *)
        exit 1
      ;;
    esac
  done
