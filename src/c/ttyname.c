#include <unistd.h>
#include <stdio.h>

int main() {
	char *tty = ttyname(STDIN_FILENO);
	printf("%s\n", tty);
	return 0;
}
