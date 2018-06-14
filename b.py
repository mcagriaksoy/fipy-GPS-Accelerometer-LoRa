from network import LoRa
from LIS2HH12 import LIS2HH12
from pytrack import Pytrack
import pycom
import socket
import binascii
import struct
import pycom
import network
import json

gc.enable()
py = Pytrack()
l76 = L76GNSS()
acc = LIS2HH12()
l76 = L76GNSS(py, timeout=10)
pycom.heartbeat(False)
x=0


#lora_packet.decrypt(packet, AppSKey, NwkSKey).toString('hex')
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
dev_addr = struct.unpack(">l", binascii.unhexlify('26011327'))[0]
nwk_swkey = binascii.unhexlify('93896830809D21A62C175C8A772053C3')
app_swkey = binascii.unhexlify('FC212CD2F15509CE2218F30A7380F58A')

lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
print ("LoRa Initialized")

while (x<1000) :

    coord = l76.coordinates()
    pitch= acc.pitch()
    roll = acc.roll()
    print('Pitch:',pitch)
    print('Roll:' ,roll)
    s.setblocking(True)
    a= pitch
    b= roll
    #x = "hi-"+str(j)+"-"+"12345678Z-"+str(coord[0]) + "-"+str(coord[1])

    p = str(coord[0])
    if p != 'None':
        #p
        if(a<0):
            la1=1
        if(b<0):
            la1=2
        b3=int(b)
        a3=int(a)

        #print('new values:',a2,b2)
        data2 = json.dumps((coord[0],coord[1],a3,b3,la1))
        #data1 = [c0,c1,a3,b3,la1]
        s.send(data2)
        print('Data sent:', data2)
        s.setblocking(False)

    else:
        pycom.rgbled(0x7f0000)
        if(a<0):
            la1=1
        if(b<0):
            la1=2
        b3=int(b)
        a3=int(a)
        #print('new values:',a2,b2)
        #data2 ="{} {} {} {}".format(c1,c2,a,b)
        data2 = [0,0,a3,b3,la1]
        s.send(bytearray(data2))
        print('Data sent:', 0,a3,b3,la1)
        s.setblocking(False)
    #rcv_data = s.recv(64)
    #print('Received lora packet:',rcv_data)
    gc.collect()
    x = x + 1
    gc.mem_free()
