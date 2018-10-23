import gpsd
import time
import logging
import json

mpstokph=3.6

# Connect to the local gpsd

logging.warning('Attempting to access GPS')
connected=False

while not connected:
    try:
        gpsd.connect()
        connected=True
    except:
        logging.critical('No GPS connection present. TIME NOT SET.')
        time.sleep(0.5)

while True:
    try:
        packet = gpsd.get_current()

        if packet.mode >= 2:
            jsonpacket = { 'timestamp': time.time(),
                     'mode': packet.mode,
                     'latitude': packet.lat,
                     'longitude': packet.lon,
                     'track': packet.track,
                     'gps_speed_kph': packet.hspeed * mpstokph,
                     'gps_time': packet.time,
                     'altitude': packet.alt }
            print(json.dumps(jsonpacket))

    except:
        logging.exception('GPS Conn Failed')

    time.sleep(1)
