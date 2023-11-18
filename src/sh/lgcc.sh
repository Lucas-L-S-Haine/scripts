#!/bin/sh
CC="${CC:-cc}"
if test "${CC}" = lgcc; then
	CC=cc
	export CC
fi
exec ${CC} -Wl,-rpath=/usr/local/lib $@
