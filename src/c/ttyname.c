#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
	int fd;
	if (argc < 2) {
		fd = 0;
	} else {
		fd = atoi(argv[1]);
	}

	if (!isatty(fd)) {
		fprintf(stderr,
				"Error: file descriptor %d is not connected to a tty\n", fd);
		return 1;
	}

	char *tty = ttyname(fd);
	printf("%s\n", tty);
	return 0;
}
