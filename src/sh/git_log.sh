#!/bin/sh

export PAGER=${PAGER:-less}
export LESS="-F -R"

git_log() {
	git log --pretty="%h %ai %s"
}

if test -t 1; then
	git_log | format-color | ${PAGER}
else
	git_log | format-nocolor
fi
