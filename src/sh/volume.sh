#!/bin/sh

urgency() {
  left_volume=$(pulsemixer --get-volume | awk '{print $1}')
  right_volume=$(pulsemixer --get-volume | awk '{print $2}')

  if test "${left_volume}" -gt 100 -o "${right_volume}" -gt 100; then
    printf '%s' critical
  else
    printf '%s' normal
  fi
}


if test "$1" = increase; then
  pulsemixer --change-volume +${2:-2} --max-volume 150
  dunstify volume "$(pulsemixer --get-volume)" \
    --replace=1 --timeout=2100 -u $(urgency)
elif test "$1" = decrease; then
  pulsemixer --change-volume -${2:-2}
  dunstify volume "$(pulsemixer --get-volume)" \
    --replace=1 --timeout=2100 -u $(urgency)
elif test -z "$1"; then
  pulsemixer --get-volume
fi
