import os
import sys
import time
import gpsd
import logging


def setgpstime():

    logging.warning('Attempting to access GPS time...')
    connected=False

    while not connected:
        try:
            gpsd.connect()
            connected=True
        except:
            logging.critical('No GPS connection present. TIME NOT SET.')
            time.sleep(0.5)

    waitingtime = True

    while waitingtime:
        try:
            packet = gpsd.get_current()

            gpstime = packet.get_time()
            timestr = str(gpstime)

            logging.warning('Setting system time to GPS time...')
            logging.warning(timestr)

            os.system('sudo date -u --set="%s"' % gpstime)
            logging.warning('System time set.')
            waitingtime=False

        except:
            logging.warning('Waiting for GPS')

        time.sleep(1)


if __name__ == '__main__':
    setgpstime()
