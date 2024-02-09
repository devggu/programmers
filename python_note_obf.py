import OpenOPC
import time
import pywintypes
pywintypes.datetime = pywintypes.TimeType
O0O0O00O000OO  = OpenOPC.client()
O0O0O00O000OO .servers()
O0O0O00O000OO .connect('Matrikon.OPC.Simulation.1')
O00O00OOOO000  = ['Random.Int1', 'Random.Real4', 'Random.Int2', 'Random.Real8']
while True:
    try:
        O0OOOO0OO000O  = O0O0O00O000OO .read(O00O00OOOO000 , group='Group0', update=1)
        print(O0OOOO0OO000O )
    except OpenOPC.TimeoutError:
        print('TimeoutError occured')
    time.sleep(1)