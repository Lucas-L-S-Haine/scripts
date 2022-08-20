LITTLER_BIN = system.file("bin", "r", package = "littler")
LITTLER_LINK = "${HOME}/.local/bin/r"
ARGS = "-s", $(LITTLER_BIN), $(LITTLER_LINK)
COMMAND = system2("ln", args = c($(ARGS)))

EEXIST = "\n\x1b[31merror:\x1b[0m file $$(which r) already exists\n"

all: install link

install:
	jetpack install

link:
	jetpack check
	if test -e "${HOME}/.local/bin/r"; then \
	printf $(EEXIST); \
	exit 1; fi
	Rscript -e '$(COMMAND)'
	printf "\n\x1b[32msuccess:\x1b[0m symbolic link created at $$(which r)\n"
