CC := gcc
CFLAGS := -Wall -Wextra -Werror

BIN_DIR := $(abspath $(CURDIR)/../../bin)

EXT := .c

SRC_FILES := $(wildcard *$(EXT))

LINKS_TXT := $(file < links.txt)

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

link: $(TARGET_FILES)

unlink: | $(BIN_DIR)
	rm -f $(TARGET_FILES)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(TARGET_FILES): | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $(call GET_SRC,$(@F))

.PHONY: link unlink

.SILENT: unlink $(TARGET_FILES)
