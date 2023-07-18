#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <sys/wait.h>
#include <sys/types.h>

int getopt(int ARGC, char *const *ARGV, const char *OPTIONS);
int optopt;
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
	if (status != 0)
		exit(status);
	kill(login_shell_pid, SIGHUP);
}

int main(int argc, char *argv[]) {
	char *command;
	int c;
	pid_t login_shell_pid;
	while ((c = getopt(argc, argv, "hp:")) != -1) {
		switch (c) {
			case 'h':
				show_help();
				return 0;
			case 'p':
				login_shell_pid = atoi(optarg);
				printf("%d\n", login_shell_pid);

				command = argv[optind];

				//char *args[argc - optind]; // TODO: fix this
				if (command == NULL) {
					fprintf(stderr, "You didn't choose a session.\n");
					return 1;
				} else {
					for (int index = optind; index < argc; index++) {
						args[index - optind] = argv[index];
					}

					printf("You chose ");
					for (int index = optind; index < argc - 1; index++) {
						printf("%s ", argv[index]);
					}
					printf("%s\n", argv[argc - 1]);
				}
				printf("%d - %d = %d\n", argc, optind, argc - optind);
				return 1;
			case '?':
				fprintf(stderr, "the option %d is not recognized",
						optopt);
				show_help();
				return 1;
			default:
				abort();
		}
	}

	char *session;
	session = argv[optind];

	if (session == NULL) {
		fprintf(stderr, "You didn't choose a session.\n");
		return 1;
	} else {
		printf("You chose ");
		for (int index = optind; index < argc - 1; index++) {
			printf("%s ", argv[index]);
		}
		printf("%s\n", argv[argc - 1]);
	}

	printf("%d - %d = %d\n", argc, optind, argc - optind);

	/*
	printf("Chosen session: ");
	for (int index = optind; index < argc; index++) {
		printf("%s ", argv[index]);
	}
	printf("\n");
	printf("argc: %d\noptind: %d\n", argc, optind);
	*/

	return 0;
}
