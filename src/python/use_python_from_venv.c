#include <unistd.h>
#include <stdio.h>

void print_array(char *array[]) {
	int index = 0;

	printf("{");
	while(array[index + 1] != NULL) {
		printf("\"%s\", ", array[index]);
		index++;
	}
	printf("\"%s\"}\n", array[index]);
}

int main(int argc, char *argv[]) {
	char *args[argc + 2];

	args[0] = "python";
	args[1] = SCRIPT;
	int index;
	for (index = 2; index < argc + 2; index++)
		args[index] = argv[index - 1];
	args[index] = NULL;

	execv(PYTHON, args);
	perror("execv");
	return 1;
}
