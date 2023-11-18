#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <alsa/asoundlib.h>

void urgency() {
}

int main() {
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

    // Get the current volume
    long min, max, volume;
    snd_mixer_selem_get_playback_volume_range(elem, &min, &max);
    snd_mixer_selem_get_playback_volume(elem, 0, &volume);

    // Print the current volume
    double human_readable_volume = 100 * volume / pow(2, 16);
    printf("Current Volume: %.lf\n", human_readable_volume);

    // Set the volume (adjust the value as needed)
    snd_mixer_selem_set_playback_volume_all(elem, volume + 10);

    // Cleanup
    snd_mixer_close(handle);

    return 0;
}
