#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <alsa/asoundlib.h>

double roundeven(double x);
long int lrint(double x);

struct Volume {
	long int min;
	long int max;
	long int left_value;
	long int right_value;
	double left_percent;
	double right_percent;
};

char *urgency(struct Volume vol) {
	if (vol.left_value > vol.max || vol.right_value > vol.max) {
		return "critical";
	} else if (vol.left_value <= vol.min && vol.right_value <= vol.min) {
		return "low";
	}

	return "normal";
}

struct Volume get_volume(snd_mixer_elem_t *elem) {
	struct Volume vol;

	snd_mixer_selem_get_playback_volume_range(elem, &vol.min, &vol.max);
	snd_mixer_selem_get_playback_volume(elem, 0, &vol.left_value);
	snd_mixer_selem_get_playback_volume(elem, 1, &vol.right_value);

	double range = (double)(vol.max - vol.min);
	long int left_offset = vol.left_value - vol.min;
	long int right_offset = vol.right_value - vol.min;

	vol.left_percent = 100 * left_offset / range;
	vol.right_percent = 100 * right_offset / range;

	return vol;
}

void increase_volume(snd_mixer_elem_t *elem, double new_volume) {
	int result;
	struct Volume vol = get_volume(elem);
	long int range = vol.max - vol.min;
	long int new_value = lrint(range * new_volume / 100.0);

	long int left = vol.left_value + new_value;
	left = left > vol.max ? vol.max : left;
	result = snd_mixer_selem_set_playback_volume(elem, 0, left);
	if (result != 0) {
		fprintf(stderr, "Error: failed to change volume.\n");
		exit(result);
	}

	long int right = vol.right_value + new_value;
	right = right > vol.max ? vol.max : right;
	result = snd_mixer_selem_set_playback_volume(elem, 1, right);
	if (result != 0) {
		fprintf(stderr, "Error: failed to change volume.\n");
		exit(result);
	}
}

void decrease_volume(snd_mixer_elem_t *elem, double new_volume) {
	int result;
	struct Volume vol = get_volume(elem);
	long int range = vol.max - vol.min;
	long int new_value = lrint(range * new_volume / 100.0);

	long int left = vol.left_value - new_value;
	left = left < vol.min ? vol.min : left;
	result = snd_mixer_selem_set_playback_volume(elem, 0, left);
	if (result != 0) {
		fprintf(stderr, "Error: failed to change volume.\n");
		exit(result);
	}

	long int right = vol.right_value - new_value;
	right = right < vol.min ? vol.min : right;
	result = snd_mixer_selem_set_playback_volume(elem, 1, right);
	if (result != 0) {
		fprintf(stderr, "Error: failed to change volume.\n");
		exit(result);
	}
}

void set_volume(snd_mixer_elem_t *elem, double new_volume) {
	int result;
	struct Volume vol = get_volume(elem);
	long int range = vol.max - vol.min;
	long int new_value = lrint(range * new_volume / 100.0);

	long int left = vol.min + new_value;
	if (left < vol.min) {
		left = vol.min;
	} else if (left > vol.max) {
		left = vol.max;
	}

	result = snd_mixer_selem_set_playback_volume(elem, 0, left);
	if (result != 0) {
		fprintf(stderr, "Error: failed to change volume.\n");
		exit(result);
	}

	long int right = vol.min + new_value;
	if (right < vol.min) {
		right = vol.min;
	} else if (right > vol.max) {
		right = vol.max;
	}

	result = snd_mixer_selem_set_playback_volume(elem, 1, right);
	if (result != 0) {
		fprintf(stderr, "Error: failed to change volume.\n");
		exit(result);
	}
}

double round_percent(double x) {
	return roundeven(100.0 * x) / 100.0;
}

double round_scale(double x, double scale) {
	return roundeven(scale * x) / scale;
}

void notify(struct Volume vol) {
	pid_t pid = fork();
	if (pid > 0) {
		char level[12];
		double left = round_percent(vol.left_percent);
		double right = round_percent(vol.right_percent);
		sprintf(level, "%.f %.f", left, right);
		char *args[] = {"notify-send", "--replace-id=1",
			"--expire-time=2100", "-u", urgency(vol),
			"volume", level, NULL};
		execvp("notify-send", args);
	}
}

int main(int argc, char **argv) {
	// Initialize ALSA mixer handle
	snd_mixer_t *handle;
	snd_mixer_open(&handle, 0);

	// Attach the mixer handle to the default sound card
	snd_mixer_attach(handle, "default");

	// Register the mixer components
	snd_mixer_selem_register(handle, NULL, NULL);

	// Load the mixer elements
	snd_mixer_load(handle);

	// Find the Master playback control
	snd_mixer_selem_id_t *sid;
	snd_mixer_selem_id_alloca(&sid);
	snd_mixer_selem_id_set_index(sid, 0);
	snd_mixer_selem_id_set_name(sid, "Master");

	snd_mixer_elem_t *elem = snd_mixer_find_selem(handle, sid);

	// Get the volume
	struct Volume vol = get_volume(elem);

	if (argc == 1) {
		printf("%.f %.f\n", round_percent(vol.left_percent),
				round_percent(vol.right_percent));
	} else if (!strcmp(argv[1], "increase")) {
		increase_volume(elem, atof(argv[2]));
		notify(get_volume(elem));
	} else if (!strcmp(argv[1], "decrease")) {
		decrease_volume(elem, atof(argv[2]));
		notify(get_volume(elem));
	} else if (!strcmp(argv[1], "set")) {
		set_volume(elem, atof(argv[2]));
		notify(get_volume(elem));
	}

	// Cleanup
	snd_mixer_close(handle);

	return 0;
}
