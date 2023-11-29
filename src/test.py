"""
Mehmet Cagri Aksoy - 2018-2023
"""

import gc
# test.py - Test the LoRaWAN functionality of the FiPy.
import time

import utime
from L76GNSS import L76GNSS
from machine import RTC, SD, Timer
from network import LoRa
from pytrack import Pytrack

""" LoRaWAN Test """
def test_function():
    """
    This function initializes the necessary components and continuously prints the coordinates, current time, and available memory.
    """
    pycom.wifi_on_boot(False)
    time.sleep(2)
    gc.enable()

    # setup rtc
    rtc = machine.RTC()
    rtc.ntp_sync("pool.ntp.org")
    utime.sleep_ms(750)
    print('\nRTC Set from NTP to UTC:', rtc.now())
    utime.timezone(7200)
    print('Adjusted from UTC to EST timezone', utime.localtime(), '\n')
    py = Pytrack()
    l76 = L76GNSS(py, timeout=30)
    chrono = Timer.Chrono()
    chrono.start()
    #sd = SD()
    #os.mount(sd, '/sd')
    #f = open('/sd/gps-record.txt', 'w')
    while (True):

        coord = l76.coordinates()
        #f.write("{} - {}\n".format(coord, rtc.now()))
        print("{} - {} - {}".format(coord, rtc.now(), gc.mem_free()))
