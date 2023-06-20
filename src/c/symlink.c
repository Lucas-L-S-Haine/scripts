#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

#define ERROR_INSUFICIENT_ARGUMENTS 1
#define ERROR_SYMLINK_CREATION 3

int file_exists(char *filepath) {
	int result = faccessat(AT_FDCWD, filepath, F_OK, AT_SYMLINK_NOFOLLOW) + 1;
	return result;
}

int main(int argc, char **argv) {
	if (argc != 3) {
		fprintf(stderr, "Error: the %s command requires two arguments.\n", argv[0]);
		return ERROR_INSUFICIENT_ARGUMENTS;
	}

	char *target = argv[1];
	char *link_name = argv[2];

	if (file_exists(link_name)) {
		fprintf(stderr, "Error: the file %s already exists.\n", link_name);
		return ERROR_SYMLINK_CREATION;
	}

	symlink(target, link_name);
	return 0;
}
