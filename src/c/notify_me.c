#include <stdio.h>
#include <libnotify/notify.h>

NotifyNotification *notify(char *summary, char *body, char *icon) {
	NotifyNotification *notif = notify_notification_new(summary, body, icon);

	if (notif) {
		notify_notification_set_timeout(notif, 21000);
		notify_notification_set_urgency(notif, NOTIFY_URGENCY_NORMAL);
	}

	return notif;
}

int main(int argc, char **argv) {
	if (argc < 3)
		return 1;

	notify_init("NotifyMe");

	NotifyNotification *notif = notify(argv[1], argv[2], NULL);
	notify_notification_show(notif, NULL);

	g_object_unref(G_OBJECT(notif));
	notify_uninit();

	return 0;
}
