"""
Mehmet Cagri Aksoy - 2018-2023
"""
import binascii
import socket
import struct
import time

import cayenneLPP
import network
import pycom
from LIS2HH12 import LIS2HH12
from network import LoRa
from pytrack import Pytrack

gc.enable()
py = Pytrack()
acc = LIS2HH12()
l76 = L76GNSS(py, timeout=10)
pycom.heartbeat(False)

""" Send Data """
def send_data():
    """
    Sends GPS and accelerometer data using LoRa communication.
    """
    #lora_packet.decrypt(packet, AppSKey, NwkSKey).toString('hex')
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868,adr=False, tx_retries=0, device_class=LoRa.CLASS_A)
    dev_addr = struct.unpack(">l", binascii.unhexlify('26011327'))[0]
    nwk_swkey = binascii.unhexlify('93896830809D21A62C175C8A772053C3')
    app_swkey = binascii.unhexlify('FC212CD2F15509CE2218F30A7380F58A')

    lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
    print ("LoRa Initialized")
    py.setup_int_pin_wake_up(False)
    py.setup_int_wake_up(True,True)
    acc.enable_activity_interrupt(150, 160)
    while True:
        #wake_s = ds.get_wake_status()
        #print(wake_s)
        time.sleep(0.1)
        if(acc.activity()):
            pycom.rgbled(0x11fff1)
            coord = l76.coordinates()
            s.setblocking(True)
            lpp = cayenneLPP.CayenneLPP(size = 100, sock = s)
            pitch= acc.pitch()
            roll = acc.roll()
            #print('Pitch:',pitch)
            #print('Roll:' ,roll)
            c0 =coord[0]
            c1 =coord[1]
            if (str(coord[0]) != 'None'):
                lpp.add_gps(c0, c1, 100.98)
                lpp.send(reset_payload = True)
                time.sleep(0.3)
                print('Data sent')
                s.setblocking(False)
            else:
                pycom.rgbled(0x7fff00)
                    #lpp.add_accelerometer(pitch,roll,0)
                lpp.add_gps(0.000000, 0.000000, 100.98, channel = 124)
                lpp.send()
                time.sleep(0.3)
                print('Data sent:')
                s.setblocking(False)
            time.sleep(0.1)
        else:
            pycom.rgbled(0x111111)
            print("SLEEP MODE ACTIVATED . . .")
            time.sleep(1)
            print(". . .")
        gc.collect()
        gc.mem_free()
           #py.setup_sleep(300)

send_data()
