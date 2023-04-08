SHELL       = node
.SHELLFLAGS = -e

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

$(BIN_DIR):
	@fs.mkdirSync("$(BIN_DIR)", { recursive: true, mode: 0o755 });

.ONESHELL:
