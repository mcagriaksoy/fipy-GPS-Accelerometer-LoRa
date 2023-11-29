"""
Mehmet Cagri Aksoy - 2018-2023
"""

import gc

from L76GNSS import L76GNSS
from pytrack import Pytrack

""" Debug """
def debug():
     gc.enable()
     py = Pytrack()

     l76 = L76GNSS(py, timeout=10)

     while(True):
          coord = l76.coordinates()
          databytes = struct.pack('d', coord[0])
          print(databytes)
          gc.collect()
