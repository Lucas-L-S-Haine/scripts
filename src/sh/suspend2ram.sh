#!/bin/sh
if test "$(id -u)" -ne 0; then
  printf 'This command is supposed to be run as root\n' >&2
  exit 1
fi

LOG_FILE="/var/log/suspend2ram.log"
> "${LOG_FILE}"
exec 2> "${LOG_FILE}"

if test -n "${DOAS_USER}"; then
  USER=${DOAS_USER}
elif test -n "${SUDO_USER}"; then
  USER=${SUDO_USER}
elif test -n $1; then
  USER=$1
else
  printf 'Unable to determine the target user\n' >&2
  exit 2
fi

# Set the DPMS timeout to 5 seconds
runuser -u ${USER} xset dpms 5 5 5

# Turn off the display
runuser -u ${USER} xset dpms force off

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
killall -SIGTERM -u ${USER}

# Wait for processes to handle SIGTERM
sleep 6

# Send SIGKILL to remaining processes
killall -SIGKILL -u ${USER}
