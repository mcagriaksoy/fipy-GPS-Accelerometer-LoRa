
import binascii
import socket
import struct

import pycom
from LIS2HH12 import LIS2HH12
from micropyGPS import MicropyGPS
from network import LoRa
from pytrack import Pytrack


def gps_lora_function():
    """ Sends GPS and accelerometer data using LoRa communication."""
    py = Pytrack()
    l76 = L76GNSS()
    acc = LIS2HH12()
    pycom.heartbeat(False)

    x = 0

    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    dev_addr = struct.unpack(">l", binascii.unhexlify('26011327'))[0]
    nwk_swkey = binascii.unhexlify('93896830809D21A62C175C8A772053C3')
    app_swkey = binascii.unhexlify('FC212CD2F15509CE2218F30A7380F58A')
    lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    print("LoRa Initialized")

    while x < 1000:
        pitch = acc.pitch()
        roll = acc.roll()
        print('Pitch:', pitch)
        print('Roll:', roll)
        s.setblocking(True)
        a = str(pitch)
        b = str(roll)  # integers, floats must convert to string to transfer
        data = "{},{}".format(a, b)
        s.send(data)

        s.setblocking(False)
        rcv_data = s.recv(64)
        print('Received lora packet:', rcv_data)
        # print('Longitude', my_gps.longitude)
        # print('Latitude', my_gps.latitude)
        lat, lon = 0.0, 0.0  # Replace with valid values
        print(lat, lon)

        x += 1
        gc.mem_free()

