#!/usr/bin/env sh

if [ -t 0 ]; then
	docker container exec -it mysql mysql "$@"
else
	docker container exec -i mysql mysql "$@"
	printf '\n'
fi
