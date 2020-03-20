#!/bin/sh

# this script must be linked here by root user
# ln -s /home/greg/Greg/work/env/projects/computerLock/computerLockWakeUp.sh /lib/systemd/system-sleep/computerLockWakeUp

export DISPLAY=:0.0
export XAUTHORITY=/home/greg/.Xauthority

case $1 in
    post)
        echo "Execute computerLock script from /lib/systemd/system-sleep"
        /home/greg/Greg/work/env/bin/computerLock --unblock
        ;;
esac
