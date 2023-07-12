#include "run.h"
#include <stdio.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>

int kill(pid_t PID, int SIGNUM);

int main() {
	char *picom[] = {"picom", NULL}; runbg("picom", picom);
	char *setxkbmap[] = {"setxkbmap", NULL}; runbg("setxkbmap", setxkbmap);
	char *numlockx[] = {"numlockx", "on", NULL}; runbg("numlockx", numlockx);

	char *wallpaper = getenv("WALLPAPER");
	if (wallpaper != NULL) {
		char *feh[] = {"feh", "--bg-scale", wallpaper, NULL};
		runbg("feh", feh);
	}

	char *dunst[] = {"dunst", NULL}; runbg("dunst", dunst);

	char *xset1[] = {"xset", "dpms", "0", "0", "0", NULL}; runbg("xset", xset1);
	char *xset2[] = {"xset", "s", "off", "-dpms", NULL}; runbg("xset", xset2);

	char *bar[] = {"dwm-status-bar", NULL}; runbg("dwm-status-bar", bar);

	char *tty = ttyname(STDIN_FILENO);
	char *dwm[] = {"dwm", NULL};
	if (tty != NULL && strcmp(tty, "/dev/tty1") == 0) {
		runfg("dwm", dwm, NULL);

		char *fish_pid_str = getenv("FISH_PID");
		if (fish_pid_str != NULL) {
			int fish_pid = atoi(fish_pid_str);
			kill(fish_pid, SIGHUP);
		}
	} else {
		execv("/usr/local/bin/dwm", dwm);
	}

	return 0;
}
