#!/bin/bash
export configfile=$1
. ${configfile}
. ${pythonenv}/bin/activate

cd ${scriptpath}

which python3

python3 ${scriptpath}/gpio_check.py || exit 1
mkdir -p ${logdir}

export timestamp=`date +%Y%m%d%H%M%S`

echo "LogID: ${timestamp} CANBUS: ${canbus}"

python3 ${scriptpath}/canlanlog.py | gzip -c > ${logdir}/gmlan_${timestamp}.json.gz

echo "Detected system powerdown or canbus activity timeout. Powering off."
date

pkill python
pkill candump

sleep 1

if mount | grep /media/usb0 > /dev/null; then
    echo "Mount detected. Syncing logs"
    sudo mkdir /media/usb0/logs
    sudo rsync -r /home/pi/logs/ /media/usb0/logs
    echo "Log sync complete"
else
    echo "No usb detected. Exiting to poweroff"
fi

# Wait for all IO.
sync; sleep 1
sync; sleep 1
sync; sleep 1

sudo poweroff


