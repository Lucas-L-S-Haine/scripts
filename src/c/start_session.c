#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <sys/wait.h>
#include <sys/types.h>

#define NO_SESSION 1
#define INVALID_OPTION 2
#define EXEC_FAIL 10

int getopt(int ARGC, char *const *ARGV, const char *OPTIONS);
int optind;
char *optarg;

int kill (pid_t PID, int SIGNUM);

void show_help(void) {
	char *help_msg =
		"start-session - a wrapper for executing your window manager from .xinitrc\n"
		"\nUsage:\n"
		"\tstart-session -h\n"
		"\tstart-session WINDOW_MANAGER [ARGS]...\n";
	printf("%s", help_msg);
}

/*
if test $(tty) = /dev/tty2; then
	dwm &
	dwm_pid=$!

	wait ${dwm_pid}

	kill -1 ${FISH_PID}
else
	exec dwm
fi
*/

pid_t runfg(char *command, char *argv[], int *status_ptr) {
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

void start_session(char *command, char *args[], pid_t login_shell_pid) {
	int status;
	runfg(command, args, &status);

	if (WIFEXITED(status)) {
		int exit_status = WEXITSTATUS(status);
		if (exit_status != 0)
			exit(exit_status);
	}

	kill(login_shell_pid, SIGHUP);
}

void print_array(char *array[], char *name, int size) {
	printf("%s: {", name);
	for (int index = 0; index < size - 1; index++)
		printf("\"%s\", ", array[index]);
	printf("\"%s\"}\n", array[size - 1]);
}

int main(int argc, char *argv[]) {
	char *command;
	int c;
	pid_t login_shell_pid;
	int args_size;
	while ((c = getopt(argc, argv, "hp:")) != -1) {
		switch (c) {
			case 'h':
				show_help();
				return 0;
			case 'p':
				login_shell_pid = atoi(optarg);
				command = argv[optind];
				args_size = argc - optind;

				if (command == NULL) {
					fprintf(stderr, "You didn't choose a session.\n");
					return NO_SESSION;
				} else {
					char *args[args_size + 1];
					for (int index = optind; index < argc; index++)
						args[index - optind] = argv[index];
					args[args_size] = NULL;
					start_session(command, args, login_shell_pid);
				}
				return 0;
			case '?':
				show_help();
				return INVALID_OPTION;
			default:
				abort();
		}
	}

	command = argv[optind];

	if (command == NULL) {
		fprintf(stderr, "You didn't choose a session.\n");
		return NO_SESSION;
	}

	args_size = argc - optind;

	char *args[args_size + 1];
	for (int index = optind; index < argc; index++)
		args[index - optind] = argv[index];
	args[args_size] = NULL;

	execvp(command, args);

	fprintf(stderr, "Error: failed to execute %s\n", command);
	return EXEC_FAIL;
}
