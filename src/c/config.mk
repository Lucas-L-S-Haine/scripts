ID != . /etc/os-release; printf '%s' "$${ID}"

ifeq ($(ID),artix)
	ifeq ($(filter notify-me,$(MAKECMDGOALS)),notify-me)
		NEW_CFLAGS = -I/usr/include/glib-2.0 -I/usr/lib/glib-2.0/include -I/usr/include/gdk-pixbuf-2.0 -pthread
		TEMP := $(CFLAGS)
		override CFLAGS += $(filter-out $(TEMP),$(NEW_CFLAGS))
		TEMP := $(LDFLAGS)
		override LDFLAGS += $(filter-out $(TEMP),-lnotify -lgobject-2.0)
	endif
endif

ifeq ($(ID),debian)
	ifeq ($(filter notify-me,$(MAKECMDGOALS)),notify-me)
		NEW_CFLAGS = -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include -I/usr/include/gdk-pixbuf-2.0 -pthread
		TEMP := $(CFLAGS)
		override CFLAGS += $(filter-out $(TEMP),$(NEW_CFLAGS))
		TEMP := $(LDFLAGS)
		override LDFLAGS += $(filter-out $(TEMP),-lnotify -lgobject-2.0)
	endif
endif

notify-me: notify_me.c
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)
