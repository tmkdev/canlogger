import logging
import datetime
import time
import json
import os

import threading
import queue

import can4python as can
import paho.mqtt.publish as publish

from pynbp import *

poweroff_timer = 30
nocan_timeout=60

nbp_kpis = {'tcs_active': None,
    'transmission_commanded_gear': None,
    'vehicle_dynamics_yaw_rate': 'Deg',
    'vdcs_over_understeer': None,
    'vdcs_active': None,
    'abs_active': None,
    'vehicle_stability_lateral_acceleration': 'g',
    'steering_wheel_angle': 'Deg',
    'accelerator_actual_position': '%',
    'boost_pressure_indication': '%',
    'platform_brake_position': '%',
    }


can_interface=os.getenv('canbus', 'can0')
kcd=os.getenv('kcd', '/home/pi/gm_global_a_hs.kcd')

bus = can.CanBus.from_kcd_file(kcd, can_interface, timeout=nocan_timeout)

statestart=datetime.datetime.now()
state = None

run = False

mqttqueue=queue.Queue()
nbpqueue=queue.Queue()

mypynbp = PyNBP(device='/dev/rfcomm0', nbpqueue=nbpqueue)
mypynbp.daemon = True
mypynbp.start()

def send_nbp(received_signalvalues):
    nbp_packet = []
    for sig in received_signalvalues:
        if sig in nbp_kpis:
            nbp_packet.append(NbpKPI(name=sig, unit=nbp_kpis[sig], value=received_signalvalues[sig]))

    if nbp_packet:
        nbpqueue.put(nbp_packet)

def send_mqtt(canqueue):
    logging.warning('Starting mqtt_sender')
    while True:
        data = canqueue.get()
        msgs=[{'topic': "candata/{0}".format(key), 'payload': value} for key, value in data.items()]
        publish.multiple(msgs, hostname="localhost")

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
        mqttqueue.put(received_signalvalues)
        send_nbp(received_signalvalues)

        print(json.dumps(received_signalvalues))

        if 'system_power_mode' in received_signalvalues:
            if state != received_signalvalues['system_power_mode']:
                state = received_signalvalues['system_power_mode']
                statestart = datetime.datetime.now()
            if not run and received_signalvalues['system_power_mode'] == 3:
                run = True
            if run and not state and  datetime.datetime.now()-statestart > datetime.timedelta(seconds=poweroff_timer):
                logging.warning('Shutdown!!')
                exit(0)

            logging.warning('Power state {0} for {1}. Run = {2}'.format(state, datetime.datetime.now()-statestart, run))

