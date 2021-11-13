#!/usr/bin/sh

CURR_DESK=$(wmctrl -d | grep '*' | cut -d '*' -f 1)

while getopts ":np" option;
  do
    case $option in
      n)
        wmctrl -s $(expr $CURR_DESK + 1)
      ;;
      p)
        if [ $CURR_DESK -gt 0 ]; then
          wmctrl -s $(expr $CURR_DESK - 1)
        fi
      ;;
      *)
        exit 1
      ;;
    esac
  done
