bin_dir := $(abspath ../../bin)

src_files := $(wildcard *.rs)
out_files := $(subst _,-,$(patsubst %.rs,$(bin_dir)/%,$(src_files)))

name_src = $(patsubst %,%.rs,$(subst -,_,$(notdir $(1))))

link: $(out_files) | $(bin_dir)

unlink:
	rm -f $(out_files)

$(bin_dir):
	if test ! -d $(bin_dir); then \
		mkdir $(bin_dir); \
	fi

$(out_files): build
	if test $@ -ot $(call name_src, $@); \
		then cp target/release/$(notdir $@) $@; \
	fi

build:
	cargo build --release

clean:
	cargo clean

debug:
	cargo build

.PHONY: link unlink build clean debug
