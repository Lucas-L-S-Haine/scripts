#!/bin/sh
CC="${CC:-gcc}"
INCLUDE="${INCLUDE:-${HOME}/.include}"
LIB="${LIB:-${HOME}/.lib}"

${CC} -I${INCLUDE} -L${LIB} -Wl,-rpath=${LIB} $@
