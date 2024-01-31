import OpenOPC
import time

import pywintypes

pywintypes.datetime = pywintypes.TimeType

opc=OpenOPC.client()

opc.servers()

opc.connect('Matrikon.OPC.Simulation.1')
tags =['Random.Int1','Random.Real4','Random.Int2','Random.Real8']
while True:
   try:
       value = opc.read(tags,group='Group0',update=1)
       print (value)
   except OpenOPC.TimeoutError:
       print ("TimeoutError occured")

   time.sleep(1)