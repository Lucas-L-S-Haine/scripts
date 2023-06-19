#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

int file_exists(char *filepath) {
	int result = faccessat(AT_FDCWD, filepath, F_OK, AT_SYMLINK_NOFOLLOW) + 1;
	return result;
}

int main(int argc, char **argv) {
	if (argc != 3) {
		fprintf(stderr, "Error: the %s command requires two arguments.\n", argv[0]);
		return 1;
	}

	char *target = argv[1];
	char *link_name = argv[2];

	if (file_exists(link_name)) {
		fprintf(stderr, "Error: the file %s already exists.\n", link_name);
		return 3;
	}

	symlink(target, link_name);
	return 0;
}
