urgency() {
	local volume_levels="$(get_volume | tr -d [%])"
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
	amixer get Master | grep -oE '\[[0-9]+%\]' | tr '\n' ' '
}

set_volume() {
	local vol="$1"
	local op="$2"
	amixer set Master "${vol}%${op}" unmute > /dev/null 2>&1
}

main() {
	if test "$1" = increase; then
		volume="$2"
		set_volume "${volume}" +
		notify-send volume "$(get_volume)" -r 1 -t 2100 -u "$(urgency)"
	elif test "$1" = decrease; then
		volume="$2"
		set_volume "${volume}" -
		notify-send volume "$(get_volume)" -r 1 -t 2100 -u "$(urgency)"
	elif test "$1" = set; then
		volume="$2"
		set_volume "${volume}"
		notify-send volume "$(get_volume)" -r 1 -t 2100 -u "$(urgency)"
	elif test -z "$1"; then
		printf '%s\n' "$(get_volume)"
	fi
}
