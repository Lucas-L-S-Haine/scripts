#!/usr/bin/sh

CURR_DESK=$(xdotool get_desktop)

while getopts ":np" option;
  do
    case $option in
      n)
        xdotool set_desktop $((CURR_DESK + 1))
      ;;
      p)
        if [ $CURR_DESK -gt 0 ]; then
          xdotool set_desktop $((CURR_DESK - 1))
        fi
      ;;
      *)
        exit 1
      ;;
    esac
  done
