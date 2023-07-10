#include "run.h"
#include <stdio.h>
#include <stdbool.h>
#include <sys/wait.h>
#include <signal.h>
#include <unistd.h>

int runbg(char *command, char *argv[]) {
	pid_t child_pid = fork();

	if (child_pid == 0) {
		execvp(command, argv);
		perror("execvp failed");
		return -1;
	} else if (child_pid < 0) {
		fprintf(stderr, "Error: failed to run %s\n", command);
		return -1;
	}

	return child_pid;
}

int runfg(char *command, char *argv[], int *status_ptr) {
	pid_t child_pid = fork();

	if (child_pid == 0) {
		execvp(command, argv);
		perror("execvp failed");
		return -1;
	} else if (child_pid < 0) {
		fprintf(stderr, "Error: failed to run %s\n", command);
		return -1;
	} else {
		waitpid(child_pid, status_ptr, 0);
	}

	return child_pid;
}
