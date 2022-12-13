littler_bin := system.file("bin", "r", package = "littler")
littler_link := "${HOME}/.local/bin/r"
args := "-s", $(littler_bin), $(littler_link)
command := system2("ln", args = c($(args)))

EEXIST = "\n\x1b[31merror:\x1b[0m file $$(which r) already exists\n"

all: install link

install:
	jetpack install

link:
	jetpack check
	if test -e "${HOME}/.local/bin/r"; then \
	printf $(EEXIST); \
	exit 1; fi
	Rscript -e '$(command)'
	printf "\n\x1b[32msuccess:\x1b[0m symbolic link created at $$(which r)\n"

lint:
	Rscript -e 'lintr::lint_dir()' >&2
