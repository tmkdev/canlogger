import time
from collections import namedtuple
import logging
import threading
import random

import serial

logger = logging.getLogger(__name__)

NbpKPI=namedtuple('NbpKPI', 'name, unit, value')

class PyNBP(threading.Thread):
    def __init__(self, nbpqueue, device='/dev/rfcomm0', device_name='PyNBP', protocol_verion='NBP1'):
        self.device = device
        self.device_name = device_name
        self.protocol_verion = protocol_verion
        self.reftime = time.time()
        self.kpis = {}
        self.nbpqueue = nbpqueue

        threading.Thread.__init__(self)


    def run(self):
        connected=False

        serport=None

        while True:
            nbpkpis = self.nbpqueue.get()

            if not connected:
                try:
                    serport=serial.Serial(self.device)
                    connected=True
                except:
                    logging.warning('Comm Port conection failed - waiting for connection')

            if connected and serport.is_open:
                nbppaket=self.update(nbpkpis)
                logging.warning(nbppaket)

                try:
                    serport.write(nbppaket)
                except:
                    logging.critical('Serial Write Failed. Closing port.')
                    serport.close()
                    connected = False


    def update(self, kpis):
        updatelist = []
        for kpi in kpis:
            updatelist.append(kpi.name)
            self.kpis[kpi.name] = kpi

        packet = self._genpacket(type='UPDATE', kpilist=updatelist)

        return packet

    def all(self):
        packet = self._genpacket(type='ALL')

        return packet

    def metedata(self):
        return str.encode("@NAME:{0}\n".format(self.device_name))

    def _genpacket(self, type='ALL', kpilist=None):
        reltime = time.time() - self.reftime
        packet="*{0},{1},{2:.3f}\n".format(self.protocol_verion, type, reltime)

        if kpilist:
            kpis = [ self.kpis[k] for k in kpilist]
        else:
            kpis = self.kpis.values()


        for kpi in kpis:
            if kpi.unit:
                packet+='"{0}","{1}":{2}\n'.format(kpi.name, kpi.unit, kpi.value)
            else:
                packet+='"{0}":{1}\n'.format(kpi.name, kpi.value)

        packet+="#\n"

        return str.encode(packet)

