bin_dir := $(abspath $(CURDIR)/../../bin)
src_files := $(wildcard *.sh)
links := $(shell cat links.txt)

get_name = $(shell grep $(1) links.txt | cut -d : -f 2)
rename = $(subst _,-,$(subst .sh,,$(1)))

name_out = $(if $(findstring $(1), $(links)), $(call get_name, $(1)), $(call rename, $(1)))
name_src = $(if $(shell grep $(1) links.txt), $(shell grep $(1) links.txt | cut -d : -f 1), $(patsubst %,%.sh,$(subst -,_,$(1))))

file_names = $(foreach file, $(src_files), $(call name_out, $(file)))

out_files = $(foreach file, $(file_names), $(bin_dir)/$(file))

link: $(out_files)

unlink: | $(bin_dir)
	rm -f $(out_files)

$(bin_dir):
	if test ! -d $(bin_dir); then \
		mkdir $(bin_dir); \
	fi

../../$(notdir $(bin_dir)): $(bin_dir)

$(bin_dir)/%: %.sh | $(bin_dir)
	ln -s $< $@

$(out_files):
	ln -s $(join $(CURDIR)/, $(call name_src, $(notdir $@))) $@
