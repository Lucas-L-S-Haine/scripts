#!/bin/sh

TIMESTAMP="$(date +%s)"
FILE="${HOME}/Pictures/screenshots/${TIMESTAMP}-print.png"


has() {
	(type $1 &> /dev/null)
	status=$?

	return ${status}
}


if ! has maim; then
	if has notify-send; then
		notify-send "Error" "maim is not installed"
	fi
	exit 1
fi


getopts s flag 2> /dev/null

case ${flag} in
	s)
		maim -us "${FILE}"
		;;
	\?)
		maim --hidecursor "${FILE}"
		;;
esac


sleep 0.1
if has notify-send; then
	notify-send --icon="${FILE}" screenshot "file available at: ${FILE}"
fi
