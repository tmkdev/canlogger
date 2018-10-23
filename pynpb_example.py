import serial
import logging
import time
import random
import queue

from pynbp import *

nbp_queue=queue.Queue()

mypynbp = PyNBP(device='/dev/rfcomm0', nbpqueue=nbp_queue)

mypynbp.daemon = True
mypynbp.start()

while True:
    testkpis = [
            NbpKPI(name='Battery', unit="V", value=random.random()*12.0),
            NbpKPI(name='Steering Wheel', unit="deg", value=random.randint(-360, 360)),
            NbpKPI(name='Gear', unit=None, value=random.randint(1,6)),
     ]

    nbp_queue.put(testkpis)

    time.sleep(1)

mypynbp.join()
