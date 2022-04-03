#!/usr/bin/env sh

if [ -t 0 ]; then
	docker container exec -it mongo mongosh --quiet "$@"
else
	docker container exec -i mongo mongosh --quiet "$@"
	printf '\n'
fi
