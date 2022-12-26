bin_dir := $(abspath ../../bin)

src_files := $(wildcard *.rs)
out_files := $(subst _,-,$(patsubst %.rs,$(bin_dir)/%,$(src_files)))

name_src = $(subst -,_,$(patsubst $(bin_dir)/%,%.rs,$(1)))

link: $(out_files)

unlink:
	rm -f $(out_files)

$(bin_dir):
	if test ! -d $(bin_dir); then \
		mkdir $(bin_dir); \
	fi

$(out_files): | $(bin_dir)
	rustc -o $@ $(call name_src, $@)

.PHONY: link unlink
