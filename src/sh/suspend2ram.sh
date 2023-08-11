#!/bin/sh
if test "$(id -u)" -ne 0; then
  printf 'This command is supposed to be run as root\n' >&2
  exit 1
fi

exec 2> /var/log/suspend2ram.log

# Set the DPMS timeout to 5 seconds
xset dpms 5 5 5

# Turn off the display
xset dpms force off

# Suspend the system
echo mem > /sys/power/state

# Wait for the system to resume
while test ! -e /sys/power/resume; do
  sleep 1
done

# Wait for the user session to be fully restored
sleep 3

# Logout the user and return to the login screen

# Send SIGTERM to user processes
if test -n "${DOAS_USER}"; then
  killall -SIGTERM -u "${DOAS_USER}"
elif test -n "${SUDO_USER}"; then
  killall -SIGTERM -u "${SUDO_USER}"
else
  printf 'Unable to determine the target user\n' >&2
  exit 2
fi

# Wait for processes to handle SIGTERM
sleep 6

# Send SIGKILL to remaining processes
if test -n "${DOAS_USER}"; then
  killall -SIGKILL -u "${DOAS_USER}"
elif test -n "${SUDO_USER}"; then
  killall -SIGKILL -u "${SUDO_USER}"
fi
