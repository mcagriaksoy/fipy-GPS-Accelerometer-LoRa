from L76GNSS import L76GNSS
from pytrack import Pytrack
import gc
gc.enable()
py = Pytrack()

l76 = L76GNSS(py, timeout=10)

while(True):
     coord = l76.coordinates()
     databytes = struct.pack('d', coord[0])
     print(databytes)
     gc.collect()
