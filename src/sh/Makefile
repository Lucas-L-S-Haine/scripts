FILES = $(wildcard *.sh)
BIN_DIR = $(shell cd ../../bin && pwd)

link:
	for FILE in $(FILES); do \
		INPUT_FILE="$(CURDIR)/$${FILE}"; \
		OUTPUT_FILE="../../bin/$$(echo "$${FILE}" | sed s/\.sh$$//)"; \
		ln -sfr "$${INPUT_FILE}" "$${OUTPUT_FILE}"; \
	done

unlink:
	for FILE in $(FILES); do \
		TARGET="$$(echo $(BIN_DIR)/$${FILE} | sed s/\.sh$$//)"; \
		rm "$${TARGET}"; \
	done
