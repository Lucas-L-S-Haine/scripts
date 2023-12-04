#!/bin/sh

MAX_VOLUME=150

urgency() {
	volume=$(amixer get Master | awk '/[0-9]+%/ {printf "%s ", $5}' | tr -d '[%]')
	left_volume=$(echo ${volume} | cut -d ' ' -f 1)
	right_volume=$(echo ${volume} | cut -d ' ' -f 2)

	if test "${left_volume}" -gt 100 -o "${right_volume}" -gt 100; then
		printf '%s' critical
	else
		printf '%s' normal
	fi
}

get_volume() {
	amixer get Master | awk '/[0-9]+%/ {printf "%s ", $5}'
}

set_volume() {
	volume=$1
	op=$2
	if ! (pactl set-sink-volume @DEFAULT_SINK@ ${op}${volume}%); then
		amixer set Master ${volume}%${op} unmute > /dev/null
	fi
}

limit_volume() {
	volume_levels=$(get_volume | tr -d [%])
	for vol in ${volume_levels}; do
		if test ${vol} -gt ${MAX_VOLUME}; then
			set_volume ${MAX_VOLUME}
		fi
	done
}

main() {
	if test "$1" = increase; then
		volume=$2
		set_volume ${volume} +
		limit_volume
		dunstify volume "$(get_volume)" --replace=1 --timeout=2100 -u "$(urgency)"
	elif test "$1" = decrease; then
		volume=$2
		set_volume ${volume} -
		dunstify volume "$(get_volume)" --replace=1 --timeout=2100 -u "$(urgency)"
	elif test "$1" = set; then
		volume="$2"
		set_volume ${volume}
		limit_volume
		dunstify volume "$(get_volume)" --replace=1 --timeout=2100 -u "$(urgency)"
	elif test -z "$1"; then
		printf '%s\n' "$(get_volume)"
	fi
}

main $@
