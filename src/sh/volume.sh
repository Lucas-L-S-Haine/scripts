#!/bin/sh

urgency() {
  left_volume=$(amixer get Master | grep -oE "[0-9]+%" | head -n 1 | tr -d '%')
  right_volume=$(amixer get Master | grep -oE "[0-9]+%" | tail -n 1 | tr -d '%')

  if test "${left_volume}" -gt 100 -o "${right_volume}" -gt 100; then
    printf '%s' critical
  else
    printf '%s' normal
  fi
}

get_volume() {
  if (type pulsemixer > /dev/null 2>&1); then
    pulsemixer --get-volume
  else
    amixer get Master | awk '/[0-9]+%/ {printf "%s ", $5}'
  fi
}

set_volume() {
  if (type pulsemixer > /dev/null 2>&1); then
    pulsemixer --change-volume $1
  else
    local volume="$(echo $1 | sed -E 's/^([+-])([0-9]+)/\2%\1/')"
    amixer set Master ${volume} unmute > /dev/null 2>&1
  fi
}

if test "$1" = increase; then
  volume=$(echo $2 | sed 's/\([0-9]\+\)/+\1/')
  set_volume ${volume}
  dunstify volume "$(get_volume)" --replace=1 --timeout=2100 -u "$(urgency)"
elif test "$1" = decrease; then
  volume=$(echo $2 | sed 's/\([0-9]\+\)/-\1/')
  set_volume ${volume}
  dunstify volume "$(get_volume)" --replace=1 --timeout=2100 -u "$(urgency)"
elif test -z "$1"; then
  get_volume
fi
