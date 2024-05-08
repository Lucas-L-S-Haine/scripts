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
		"\tstart-session WINDOW_MANAGER [ARGS]...\n"
		"\tstart-session -p LOGIN_SHELL_PID WINDOW_MANAGER [ARGS]...\n"
		"\nOptions:\n"
		"\t-h\n"
		"\t\tShow this help message and exit.\n"
		"\t-p LOGIN_SHELL_PID\n"
		"\t\tRun the window manager as a child process, wait for its\n"
		"\t\tcompletion, then send a SIGHUP to LOGIN_SHELL_PID.\n"
		"\nDescription:\n"
		"\tstart-session takes a window manager as an argument and executes it."
		"\n\tWith the -p option, it takes the pid of the login shell, runs the"
		"\n\twindow manager as a child process in the foreground, then sends the"
		"\n\tlogin shell a SIGHUP after the window manager exits. That way, the"
		"\n\tuser is sent back to the login screen on the tty. This program is"
		"\n\tmeant to be exec'd from .xinitrc.\n"
		"\nExamples:\n"
		"\t1. exec start-session spectrwm\n"
		"\t2. if test $(tty) = /dev/tty1; then\n"
		"\t       exec start-session -p ${BASH_PID} dwm\n"
		"\t   fi\n";
	printf("%s", help_msg);
}

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

	if (login_shell_pid != 0)
		kill(login_shell_pid, SIGHUP);
}

void print_array(char *array[], char *name, int size) {
	printf("%s: {", name);
	for (int index = 0; index < size - 1; index++)
		printf("\"%s\", ", array[index]);
	printf("\"%s\"}\n", array[size - 1]);
}

void handle_sigchld() {
	while (waitpid(-1, NULL, WNOHANG) > 0);
}

int main(int argc, char *argv[]) {
	char *command;
	int c;
	pid_t login_shell_pid;
	int args_size;

	signal(SIGCHLD, handle_sigchld);

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

	start_session(command, args, 0);

	fprintf(stderr, "Error: failed to execute %s\n", command);
	return EXEC_FAIL;
}
