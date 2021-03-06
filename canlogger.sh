#!/bin/bash
export configfile=$1
. ${configfile}
. ${pythonenv}/bin/activate

cd ${scriptpath}

which python

python ${scriptpath}/gpstime3.py
python ${scriptpath}/gpio_check.py || exit 1

export timestamp=`date +%Y%m%d%H%M%S`

echo "LogID: ${timestamp} CANBUS: ${canbus}"

/usr/bin/candump -L ${canbus} | gzip -c > ${logdir}/rawlog_${timestamp}.candump.gz &
python ${scriptpath}/gpslogger.py | gzip -c > ${logdir}/gps_${timestamp}.json.gz &

python ${scriptpath}/canlanlog.py | gzip -c > ${logdir}/gmlan_${timestamp}.json.gz

echo "Detected system powerdown or canbus activity timeout. Powering off."
date

pkill python
pkill candump

sleep 1

#Purge 0 length files.
find /home/pi/logs/ -type f -size -40c -delete

if mount | grep /media/usb0 > /dev/null; then
    echo "Mount detected. Syncing logs"
    date
    mkdir /media/usb0/logs
    rsync -r /home/pi/logs/ /media/usb0/logs

    find /media/usb0/logs/ -type f -size -40c -delete
    echo "Log sync complete"
    date
else
    echo "No usb detected. Exiting to poweroff"
fi

cp /home/pi/canlogger.log /home/pi/logs/canlogger_${timestamp}.log
cp /home/pi/pynbp.log /home/pi/logs/pynbp_${timestamp}.log

# Wait for all IO.
sync; sleep 1
sync; sleep 1
sync; sleep 1

sudo poweroff


