#!/bin/sh

if pactl info > /dev/null 2>&1; then
	. ~/.bin/volume-pulse
else
	. ~/.bin/volume-alsa
fi

main $@
