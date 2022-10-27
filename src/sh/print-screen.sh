#!/usr/bin/env dash

TIMESTAMP="$(date +%s)"
FILE="${HOME}/Pictures/screenshots/${TIMESTAMP}-print.png"

maim "${FILE}"

sleep 0.1
notify-send --icon="${FILE}" screenshot "file available at: ${FILE}"
