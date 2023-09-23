#!/bin/sh

getopts s: flag 2> /dev/null
case ${flag} in
	s)
		CLIENT="emacsclient -a false -s ${OPTARG}"
		shift 2;;
	\?)
		CLIENT="emacsclient -a false";;
esac

exec ${CLIENT} -e "(kill-emacs ${1:-0})"
