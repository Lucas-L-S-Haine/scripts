littler_bin := $(shell Rscript -e 'cat(system.file("bin", "r", package = "littler"))')
littler_link := "${HOME}/.local/bin/r"

bin_dir := $(abspath $(CURDIR)/../../bin)
ext := .R
src_files := $(wildcard *$(ext))
links := $(shell cat links.txt)

get_name = $(shell grep $(1) links.txt | cut -d : -f 2)
rename = $(subst _,-,$(subst $(ext),,$(1)))

name_out = $(if $(findstring $(1), $(links)), $(call get_name, $(1)), $(call rename, $(1)))
name_src = $(if $(shell grep $(1) links.txt), $(shell grep $(1) links.txt | cut -d : -f 1), $(patsubst %,%$(ext),$(subst -,_,$(1))))

file_names = $(foreach file, $(src_files), $(call name_out, $(file)))

out_files = $(foreach file, $(file_names), $(bin_dir)/$(file))

all: install link

install:
	jetpack install

link: $(out_files) $(littler_link)

unlink: | $(bin_dir)
	rm -f $(out_files) $(littler_link)

lint:
	Rscript -e 'lintr::lint_dir()' >&2

r: $(littler_link)

$(bin_dir):
	if test ! -d $(bin_dir); then \
		mkdir $(bin_dir); \
	fi

../../$(notdir $(bin_dir)): $(bin_dir)

$(bin_dir)/%: %$(ext) | $(bin_dir)
	ln -s $< $@

$(out_files):
	ln -s $(join $(CURDIR)/, $(call name_src, $(notdir $@))) $@

$(littler_link): $(littler_bin)
	ln -sf $< $@
