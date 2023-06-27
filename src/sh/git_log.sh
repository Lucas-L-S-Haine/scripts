#!/bin/sh

export PAGER=${PAGER:-less}
export LESS="-F -R"

git_log() {
	git log --pretty="%h %ai %s"
}

if test -t 1; then
	git_log | ./format_color.awk | ${PAGER}
else
	git_log | ./format_nocolor.awk
fi
