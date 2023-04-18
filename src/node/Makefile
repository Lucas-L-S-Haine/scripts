SHELL       := /usr/bin/node
.SHELLFLAGS := -e

# turn $(MAKE) into a namespace for the "make" function
define MAKE :=
	function handleRecipe(err, stdout, stderr) {
		if (err) {
			console.error(stderr.trim());
			process.exit(err.code);
		}
		console.log(stdout.trim());
	}
	const make = (args = "", options = {}) => child_process
	.execFile("$(MAKE)", args.split(/\s+/), options, handleRecipe);
endef

BIN_DIR := $(abspath $(CURDIR)/../../bin)

EXT = %.js %.cjs %.mjs %.ts
JS_FILES := $(wildcard $(subst %,*,$(EXT)))

OK = fs.constants.R_OK + fs.constants.X_OK
define IS_EXEC
$(shell
	try {
		fs.accessSync("$1", $(OK));
		console.log("$1");
	} catch {
		null;
	}
)
endef

define SRC_FILES :=
$(strip
	$(foreach FILE,
		$(filter $(EXT), $(JS_FILES)),
		$(call IS_EXEC,$(FILE))
	)
)
endef

LINKS_TXT = $(file < links.txt)

define LINKED_FILES :=
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

define CHECK_DUPLICATES
$(foreach LINK,$(OUT_FILES),
	$(intcmp 1,
		$(words $(filter $(LINK),$(OUT_FILES))),
		$(error There are two or more output files with the same name)
	)
)
endef
$(CHECK_DUPLICATES)

# get output files and return corresponding source from links.txt
GET_LINKED_SRC = $(firstword $(subst :, ,$(filter %:$1,$(file < links.txt))))

define GET_FILE_NAME
$(strip
	$(filter $(subst -,_,$(notdir $1)).%,
		$(filter-out $(LINKED_FILES),$(JS_FILES))
	)
)
endef

# either get source name from links.txt or use subst on link's name
define GET_SRC
$(strip
	$(if $(call GET_LINKED_SRC,$1),
		$(call GET_LINKED_SRC,$1),
		$(call GET_FILE_NAME,$1)
	)
)
endef

TARGET_FILES := $(foreach FILE,$(OUT_FILES),$(BIN_DIR)/$(FILE))

all: link

link: $(TARGET_FILES)

unlink: | $(BIN_DIR)
	for (const link of "$(TARGET_FILES)".split(/\s+/)) {
		if (fs.existsSync(link)) {
			fs.unlinkSync(link);
		}
	}

$(BIN_DIR):
	fs.mkdirSync(`$(BIN_DIR)`, { recursive: true, mode: 0o755 });

$(TARGET_FILES): | $(BIN_DIR)
	process.chdir(`$(BIN_DIR)`);
	fs.symlinkSync("../src/node/$(call GET_SRC,$(notdir $@))", "$(notdir $@)");

.PHONY: all link unlink

.SILENT: unlink $(TARGET_FILES)

.ONESHELL:
