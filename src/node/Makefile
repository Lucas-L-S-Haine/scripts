SHELL       = node
.SHELLFLAGS = -e

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

all: link

# create symbolic links at target directory
link:

# remove symbolic links
unlink:

$(BIN_DIR):
	@fs.mkdirSync(`$(BIN_DIR)`, { recursive: true, mode: 0o755 });

.PHONY: all link unlink

.ONESHELL:
