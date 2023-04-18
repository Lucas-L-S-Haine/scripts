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
		$(filter $(EXT), $(wildcard *)),
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

all: link

# create symbolic links at target directory
link:

# remove symbolic links
unlink:

$(BIN_DIR):
	@fs.mkdirSync(`$(BIN_DIR)`, { recursive: true, mode: 0o755 });

.PHONY: all link unlink

.ONESHELL:
