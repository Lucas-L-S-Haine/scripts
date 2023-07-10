#include "run.h"
#include <stdio.h>
#include <sys/wait.h>

int main() {
	int status;
	char *argv[] = {"notify-send", "message", "Hello, World!", NULL};
	runfg("/usr/bin/notify-send", argv, &status);

	return 0;
}
