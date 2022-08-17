#!/usr/bin/env sh

curl \
    -d "${1}" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    "${2}"
