#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdbool.h>
#include <string.h>
#include <fcntl.h>
#include <sys/ioctl.h>

char *basename(const char *filename);

typedef struct {
	char name[256];
	pid_t pid;
	pid_t ppid;
} Process;

bool is_init(Process process) {
	return process.pid == 1;
}

bool is_login(Process process) {
	return strcmp(process.name, "login") == 0;
}

bool process_is_connected_to_tty(Process process, int fd) {
	char terminal_symlink[256];
	sprintf(terminal_symlink, "/proc/%d/fd/%d", process.pid, fd);

	int terminal_fd = open(terminal_symlink, O_NOCTTY);
	bool is_tty = isatty(terminal_fd);

	close(terminal_fd);

	return is_tty;
}

char *get_ttyname_from_process(Process process, int fd) {
	char terminal_symlink[256];
	sprintf(terminal_symlink, "/proc/%d/fd/%d", process.pid, fd);

	int terminal_fd = open(terminal_symlink, O_NOCTTY);
	char *terminal_device_name = ttyname(terminal_fd);

	close(terminal_fd);
	
	return terminal_device_name;
}

Process get_process_from_pid(pid_t pid) {
	char file[25];
	sprintf(file, "/proc/%d/stat", pid);

	FILE *status_file = fopen(file, "r");

	int proc_pid;
	int proc_ppid;
	char proc_name[256];

	fscanf(status_file, "%d %*[(] %s %*c %d",
			&proc_pid, proc_name, &proc_ppid);

	int index = 0;
	while (proc_name[index]) {
		if (proc_name[index] == ')')
			proc_name[index] = '\0';
		index++;
	}

	Process process;
	process.pid = proc_pid;
	process.ppid = proc_ppid;
	strcpy(process.name, proc_name);

	fclose(status_file);

	return process;
}

char *seek_tty(pid_t pid, int fd) {
	Process process = get_process_from_pid(pid);

	while (!is_init(process) && !is_login(process)) {
		if (process_is_connected_to_tty(process, fd))
			return get_ttyname_from_process(process, fd);

		process = get_process_from_pid(process.ppid);
	}

	return NULL;
}

void show_info(char *tty_name, int lines, int columns) {
	printf("tty: %s\nlines: %d\ncolumns: %d\n", tty_name, lines, columns);
}

int main(int argc, char *argv[]) {
	char *name = basename(argv[0]);

	int fd;
	if (argc == 1)
		fd = 0;
	else
		fd = atoi(argv[1]);

	char *tty_name = seek_tty(getpid(), fd);
	if (tty_name == NULL) {
		fprintf(stderr, "No parent process is connected to a tty.\n");
		return 1;
	}

	int tty_fd = open(tty_name, O_NOCTTY);

	struct winsize window_size;
	ioctl(tty_fd, TIOCGWINSZ, &window_size);

	close(tty_fd);

	if (!strcmp(name, "tty-name"))
		printf("%s\n", tty_name);
	else if (!strcmp(name, "tty-cols"))
		printf("%d\n", window_size.ws_col);
	else if (!strcmp(name, "tty-rows"))
		printf("%d\n", window_size.ws_row);
	else
		show_info(tty_name, window_size.ws_row, window_size.ws_col);

	return 0;
}
