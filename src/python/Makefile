SHELL       := /usr/bin/python3
.SHELLFLAGS := -c

# turn $(MAKE) into a namespace for the "make" function
define MAKE :=
	from subprocess import run as _run
	def make(args: str):
		_run(["$(MAKE)", *args.split()])
endef

define PIP :=
	from sys import executable as python
	from subprocess import run as _run
	def pip(args: str):
		_run([python, "-m", "pip", *args.split()])
endef

OS := import os

OK = os.R_OK + os.X_OK
IS_EXEC = $(shell $(OS); print("$1") if os.access("$1", $(OK)) else None)

BIN_DIR := $(abspath $(CURDIR)/../../bin)

EXT = .py

define SRC_FILES
$(strip
	$(foreach FILE, $(wildcard *$(EXT)),
		$(call IS_EXEC,$(FILE))
	)
)
endef

LINKS_TXT = $(file < links.txt)

define LINKED_FILES
$(strip
	$(foreach FILE, $(LINKS_TXT),
		$(firstword
			$(subst :, ,$(FILE))
		)
	)
)
endef

# create link names from links.txt
define OUT_FILES :=
$(strip
	$(foreach FILE, $(LINKS_TXT),
		$(word 2,
			$(subst :, ,$(FILE))
		)
	)
)
endef

# add files that are not listed in links.txt
define OUT_FILES +=
$(strip
	$(basename
		$(subst _,-,
			$(filter-out $(LINKED_FILES),
				$(SRC_FILES)
			)
		)
	)
)
endef

# get output files and return corresponding source from links.txt
GET_LINKED_SRC = $(firstword $(subst :, ,$(filter %:$1,$(file < links.txt))))

# either get source name from links.txt or use subst on link's name
define GET_SRC
$(strip
	$(if $(call GET_LINKED_SRC,$1),
		$(call GET_LINKED_SRC,$1),
		$(subst -,_,$1)$(EXT)
	)
)
endef

TARGET_FILES := $(foreach FILE,$(OUT_FILES),$(BIN_DIR)/$(FILE))

all: install link

install: requirements.txt
	$(PIP)
	pip("install -r $<")

link: $(TARGET_FILES)

unlink: | $(BIN_DIR)
	$(OS)
	for link in "$(TARGET_FILES)".split():
	    if os.path.lexists(link):
	        os.unlink(link)

$(BIN_DIR):
	$(OS)
	os.makedirs("$(BIN_DIR)")

$(TARGET_FILES): | $(BIN_DIR)
	$(OS)
	os.chdir("$(BIN_DIR)")
	os.symlink("../src/python/$(call GET_SRC,$(notdir $@))", "$(notdir $@)")

.PHONY: all install link unlink

.SILENT: install unlink $(TARGET_FILES)

.ONESHELL:
