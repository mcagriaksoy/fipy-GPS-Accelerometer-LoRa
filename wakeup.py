from pytrack import Pytrack
#from pysense import Pysense
from LIS2HH12 import LIS2HH12
import pycom
import time
pycom.heartbeat(False)
py.setup_int_pin_wake_up(True)
py.setup_int_wake_up(True, False)

py = Pytrack()
acc = LIS2HH12()

acc.enable_activity_interrupt(2000, 200)
    #py.setup_sleep(30)
if(acc.activity()):
    pycom.rgbled(0xFF0000)
    print("Wake Up Reason:",str(py.get_wake_reason()) )  
else:
    print("Sleeping..." )
    py.setup_sleep(60)
    py.go_to_sleep()
