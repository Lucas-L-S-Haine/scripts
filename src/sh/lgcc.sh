#!/bin/sh
CC="${CC:-gcc}"
exec ${CC} -Wl,-rpath=/usr/local/lib $@
