MAX_VOLUME=150

urgency() {
	local volume_levels="$(get_volume | tr -d %)"
	local max="$(get_max_volume ${volume_levels})"
	if test "${max}" -eq 0; then
		printf 'low'
	elif test "${max}" -gt 100; then
		printf 'critical'
	else
		printf 'normal'
	fi
}

get_max_volume() {
	local volume_levels="$@"
	local max=0
	for vol in ${volume_levels}; do
		if test "${vol}" -gt "${max}"; then
			max="${vol}"
		fi
	done
	printf '%d' ${max}
}

get_volume() {
	pactl get-sink-volume @DEFAULT_SINK@ | grep -oE '[0-9]+%' | tr '\n' ' '
}

set_volume() {
	local vol="$1"
	local op="$2"
	pactl set-sink-volume @DEFAULT_SINK@ "${op}${vol}%"
}

print_volume() {
	printf '[%3d%%] ' $(get_volume | tr -d %)
}

limit_volume() {
	local volume_levels="$(get_volume | tr -d %)"
	local max="$(get_max_volume ${volume_levels})"
	if test "${max}" -gt "${MAX_VOLUME}"; then
		set_volume "${MAX_VOLUME}"
	fi
}

main() {
	if test "$1" = increase; then
		volume="$2"
		set_volume "${volume}" +
		limit_volume
		notify-send volume "$(print_volume)" -r 1 -t 2100 -u "$(urgency)"
	elif test "$1" = decrease; then
		volume="$2"
		set_volume "${volume}" -
		notify-send volume "$(print_volume)" -r 1 -t 2100 -u "$(urgency)"
	elif test "$1" = set; then
		volume="$2"
		set_volume "${volume}"
		notify-send volume "$(print_volume)" -r 1 -t 2100 -u "$(urgency)"
	elif test -z "$1"; then
		printf '%s\n' "$(print_volume)"
	fi
}
