import logging
import datetime
import time
import json
import os

import threading
import queue

import can4python as can
import paho.mqtt.publish as publish

from configuration import *
from pynbp import *

can_interface=configs['canbus']

bus = can.CanBus.from_kcd_file(configs['kcd'],
    can_interface,
    timeout=int(configs['nocan_timeout']))

mqttqueue=queue.Queue()
nbpqueue=queue.Queue()

def send_nbp(received_signalvalues):
    nbp_packet = []
    for sig in received_signalvalues:
        if sig in nbp_kpis:
            nbp_packet.append(NbpKPI(name=sig,
                                        unit=nbp_kpis[sig],
                                        value=received_signalvalues[sig]))

    # Send ALL updates - min_interval will keep updates to 0.2s
    if nbp_packet:
        nbpqueue.put(NbpPayload(timestamp=received_signalvalues['timestamp'],
                     packettype='UPDATE',
                     nbpkpilist=nbp_packet))

def send_mqtt(canqueue):
    logging.warning('Starting mqtt_sender')
    while True:
        data = canqueue.get()
        msgs=[{'topic': "candata/{0}".format(key), 'payload': value} for key, value in data.items()]
        publish.multiple(msgs, hostname="localhost")


if __name__ == '__main__':
    statestart=datetime.datetime.now()
    state = None
    run = False

    if configs['nbp_enable'] == '1':
        if 'serial' in configs:
            logging.warning('Starting Serial/Bluetooth NBP server')
            mypynbp = PyNBP(device=configs['serial'], nbpqueue=nbpqueue, min_update_interval=0.05)

        if 'ip' in configs:
            logging.warning('Starting Wifi NBP server')
            mypynbp = WifiPyNBP(ip=configs['ip'], port=int(configs['port']), nbpqueue=nbpqueue, min_update_interval=0.05)

        logging.warning('Starting nbp server')
        mypynbp.daemon = True
        mypynbp.start()


    if configs['mqtt_enable'] == '1':
        logging.warning('Enabling MQTT output')
        t = threading.Thread(target=send_mqtt, args=(mqttqueue, ),  daemon=True)
        t.start()

    while True:
        try:
            received_signalvalues = bus.recv_next_signals()
        except:
            logging.warning('No packets for timeout secs.. Exiting.')
            break

        if received_signalvalues:
            received_signalvalues['timestamp'] = time.time()
            if configs['mqtt_enable']:
                mqttqueue.put(received_signalvalues)
            if configs['nbp_enable']:
                send_nbp(received_signalvalues)

            print(json.dumps(received_signalvalues))

            if 'system_power_mode' in received_signalvalues:
                if state != received_signalvalues['system_power_mode']:
                    state = received_signalvalues['system_power_mode']
                    statestart = datetime.datetime.now()
                if not run and received_signalvalues['system_power_mode'] == 3:
                    run = True
                if run and not state and datetime.datetime.now() - statestart > datetime.timedelta(seconds=int(configs['poweroff_timer'])):
                    logging.warning('System off powerdown.')
                    exit(0)

                logging.warning('Power state {0} for {1}. Run = {2}'.format(state, datetime.datetime.now()-statestart, run))
