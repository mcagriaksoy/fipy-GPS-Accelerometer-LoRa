from network import LoRa
from LIS2HH12 import LIS2HH12
from pytrack import Pytrack
import pycom
import socket
import binascii
import struct
import pycom
import network
import cayenneLPP

gc.enable()
py = Pytrack()

l76 = L76GNSS()
acc = LIS2HH12()
l76 = L76GNSS(py, timeout=10)
pycom.heartbeat(False)
x=0


#lora_packet.decrypt(packet, AppSKey, NwkSKey).toString('hex')
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868,adr=False, tx_retries=0, device_class=LoRa.CLASS_A)
dev_addr = struct.unpack(">l", binascii.unhexlify('26011327'))[0]
nwk_swkey = binascii.unhexlify('93896830809D21A62C175C8A772053C3')
app_swkey = binascii.unhexlify('FC212CD2F15509CE2218F30A7380F58A')

lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
print ("LoRa Initialized")
la1=0
while (x<1000) :

    coord = l76.coordinates()
    pitch= acc.pitch()
    roll = acc.roll()
    print('Pitch:',pitch)
    print('Roll:' ,roll)
    s.setblocking(True)
    lpp = cayenneLPP.CayenneLPP(size = 100, sock = s)
    p = str(coord[0])
    if p != 'None':

        data2 = json.dumps((coord[0],coord[1],a3,b3,la1))
        lpp.add_accelerometer(pitch,roll,0)
        lpp.add_gps(coord[0], coord[1], 100.98, channel = 124)
        lpp.send(reset_payload = True)
        print('Data sent:')
        s.setblocking(False)

    else:
        pycom.rgbled(0x7f0000)
        lpp.add_accelerometer(pitch,roll,0)
        lpp.add_gps(coord[0], coord[1], 100.98, channel = 124)
        lpp.send(reset_payload = True)
        print('Data sent:')
        s.setblocking(False)
    rcv_data = s.recv(64)
    print('Received lora packet:',rcv_data)
    gc.collect()
    x = x + 1
    gc.mem_free()
