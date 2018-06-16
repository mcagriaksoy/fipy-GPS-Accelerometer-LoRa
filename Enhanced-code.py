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
import time
from deepsleep import DeepSleep
import deepsleep

ds = DeepSleep()
gc.enable()
py = Pytrack()
l76 = L76GNSS()
acc = LIS2HH12()
l76 = L76GNSS(py, timeout=10)
pycom.heartbeat(False)

#lora_packet.decrypt(packet, AppSKey, NwkSKey).toString('hex')
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868,adr=False, tx_retries=0, device_class=LoRa.CLASS_A)
dev_addr = struct.unpack(">l", binascii.unhexlify('ASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'))[0]
nwk_swkey = binascii.unhexlify('ASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
app_swkey = binascii.unhexlify('ASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')

lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
print ("LoRa Initialized")
py.setup_int_pin_wake_up(False)
py.setup_int_wake_up(True,False)
acc.enable_activity_interrupt(2500, 400)
while True:
    #wake_s = ds.get_wake_status()
    #print(wake_s)
    s.setblocking(True)
    lpp = cayenneLPP.CayenneLPP(size = 100, sock = s)
    if(acc.activity()):
        x=1
    else:
        x=0
    while(x==1):
        pycom.rgbled(0x11fff1)
        coord = l76.coordinates()
        pitch= acc.pitch()
        roll = acc.roll()
        print('Pitch:',pitch)
        print('Roll:' ,roll)
        c0 =coord[0]
        c1 =coord[1]
        if (str(coord[0]) != 'None'):
            lpp.add_gps(c0, c1, 100.98)
            lpp.send(reset_payload = True)
            print('Data sent:')
            s.setblocking(False)
        else:
            pycom.rgbled(0x7fff00)
                #lpp.add_accelerometer(pitch,roll,0)
            lpp.add_gps(0, 0, 100.98, channel = 124)
            lpp.send()
            print('Data sent:')
            s.setblocking(False)
            if(acc.activity()):
                x=1
            else:
                x=0
        time.sleep(1)
        #rcv_data = s.recv(64)
        #print('Received lora packet:',rcv_data)
    gc.collect()
    gc.mem_free()
    pycom.rgbled(0x111111)
    print("SLEEP MODE ACTIVATED . . .")
    time.sleep(0.5)
        #py.setup_sleep(300)
