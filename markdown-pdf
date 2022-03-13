#!/usr/bin/env sh

INPUT_FILE="${1}"
OUTPUT_FILE="$(echo ${INPUT_FILE} | cut -d . -f 1).pdf"

if [ "${INPUT_FILE}" = "${OUTPUT_FILE}" ]; then
	echo 'Error: cannot convert pdf files'
    exit 1
fi

pandoc "${INPUT_FILE}" \
	--from=markdown \
	--to=pdf \
	--output="${OUTPUT_FILE}" \
	--pdf-engine=xelatex \
	-V mainfont='DejaVuSans'
