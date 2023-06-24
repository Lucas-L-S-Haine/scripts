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

if test "$1" = increase; then
  amixer set Master "${2:-2}"%+ unmute
  dunstify volume "$(amixer get Master | awk '/[0-9]+%/ {print $5}')" \
    --replace=1 --timeout=2100 -u "$(urgency)"
elif test "$1" = decrease; then
  amixer set Master "${2:-2}"%- unmute
  dunstify volume "$(amixer get Master | awk '/[0-9]+%/ {print $5}')" \
    --replace=1 --timeout=2100 -u "$(urgency)"
elif test -z "$1"; then
  amixer get Master | grep -oE "[0-9]+%"
fi
