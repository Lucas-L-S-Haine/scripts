#!/usr/bin/sh

SEARCH=$(echo "$@" | tr ' ' '+')

xdg-open https://search.brave.com/search?q="$SEARCH" > /dev/null 2>&1 &
