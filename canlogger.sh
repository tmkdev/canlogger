#!/bin/bash
. $HOME/candy/bin/activate

export scriptpath=$HOME/canlogger/
export kcd=/home/pi/gm_global_a_hs.kcd

cd $scriptpath

which python

python $scriptpath/gpstime3.py
python $scriptpath/gpio_check.py || exit 1

export timestamp=`date +%Y%m%d%H%M%S`
export canbus=can0
export kcd=/home/pi/gm_global_a_hs.kcd

echo $timestamp $canbus

/usr/bin/candump -L ${canbus} | gzip -c > $HOME/logs/rawlog_${timestamp}.candump.gz &
python  $scriptpath/gpslogger.py | gzip -c > $HOME/logs/gps_${timestamp}.json.gz &

python $scriptpath/gmlanlog.py | gzip -c > $HOME/logs/gmlan_${timestamp}.json.gz

echo "Detected system powerdown or canbus activity timeout. Powering off."
date

pkill python
pkill candump

sleep 1

if mount | grep /media/usb0 > /dev/null; then
    echo "Mount detected. Syncing logs"
    sudo mkdir /media/usb0/logs
    sudo rsync -r /home/pi/logs/ /media/usb0/logs
else
    echo "No usb detected. Exiting to poweroff"
fi

# Wait for all IO.
sync; sleep 1
sync; sleep 1
sync; sleep 1

sudo poweroff


