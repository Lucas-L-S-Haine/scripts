#!/bin/sh

getopts s: flag 2> /dev/null
case ${flag} in
	s)
		SERVER=${OPTARG}
		CLIENT="emacsclient -a false -s ${SERVER}"
		shift 2;;
	\?)
		CLIENT="emacsclient -a false";;
esac

if test -n "${SERVER}"; then
	${CLIENT} -e "(kill-emacs 0)" && emacs --daemon=${SERVER}
else
	${CLIENT} -e "(kill-emacs 0)" && emacs --daemon
fi
