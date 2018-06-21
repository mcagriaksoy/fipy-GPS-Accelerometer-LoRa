#import libraries:
from network import LoRa
from LIS2HH12 import LIS2HH12 #Accelerometer
from L76GNSS import L76GNSS #GPS
from pytrack import Pytrack
from deepsleep import DeepSleep
import deepsleep
import pycom
import socket
import struct
import pycom
import binascii
import network
import cayenneLPP #Low power packet forwarding
import time
from network import Bluetooth
import gc
import math
#Enable garbage collection:
gc.enable()
gc.collect()

#Close Unnecessary functions:
ds = DeepSleep()
ds.enable_auto_poweroff()
#enable auto power off then li-po can't supply 3.3v
bt = Bluetooth()
bt.deinit() #close bluetooth
wlan = network.WLAN() #close wlan
wlan.deinit()

py = Pytrack()
acc = LIS2HH12()
l76 = L76GNSS(py, timeout=10)

pycom.heartbeat(False)
ds.enable_auto_poweroff()
#lora_packet.decrypt(packet, AppSKey, NwkSKey).toString('hex')

#Lora settings:
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868,adr=False, tx_retries=0, device_class=LoRa.CLASS_A)
dev_addr = struct.unpack(">l", binascii.unhexlify('26011327'))[0]
nwk_swkey = binascii.unhexlify('93896830809D21A62C175C8A772053C3')
app_swkey = binascii.unhexlify('FC212CD2F15509CE2218F30A7380F58A')
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
print ("LoRa Initialized")

#Accelerometer wake-up settings:
py.setup_int_pin_wake_up(False)
py.setup_int_wake_up(True,True)
acc.enable_activity_interrupt(150, 160)
while True:
    #wake_s = ds.get_wake_status()
    #print(wake_s)
    time.sleep(0.1)
    if(acc.activity()):
        pycom.rgbled(0x11fff1)
        s.setblocking(True)
        lpp = cayenneLPP.CayenneLPP(size = 100, sock = s) #create socket to send messages to server
        pitch= acc.pitch()
        roll = acc.roll()
        x,y,z = acc.acceleration()

        #if (x > y) and (x > z):
        #    largest = x
        #elif (y > x) and (y > z):
        #    largest = y
        #else:
        #    largest = z
        time.sleep(0.02)
        x1,y1,z1 = acc.acceleration()
        time.sleep(0.02)
        x2,y2,z2 = acc.acceleration()
        time.sleep(0.02)
        x3,y3,z3 = acc.acceleration()

        #Find 4 sampled x,y,z values:

        xsum = (x+x1+x2+x3) / 4
        ysum = (y+y1+y2+y3) / 4
        zsum = (z+z1+z2+z3) / 4

        gtotal = math.sqrt(xsum * xsum + ysum * ysum + zsum * zsum) #Measure G total force

        print("A:",abs(gtotal-1))
        #print('Pitch:',pitch)
        #print('Roll:' ,roll)
        c0 =coord[0]
        c1 =coord[1]
        volt= py.read_battery_voltage() #Read Battery Voltage
        print(xsum,ysum,zsum)
        coord = l76.coordinates() #Get the coordinates
        if (str(coord[0]) != 'None'):
            pycom.rgbled(0x7fff00)
            lpp.add_accelerometer(xsum,ysum,zsum)

            lpp.add_analog_input(abs(gtotal-1))
            lpp.add_analog_input(volt, channel = 114)
            lpp.add_gps(c0, c1, 55)
            lpp.send()
            time.sleep(0.1)
            #print('Data sent')
        else:
            pycom.rgbled(0xde0000)
            lpp.add_accelerometer(xsum,ysum,zsum)
            lpp.add_analog_input(abs(gtotal-1))
            lpp.add_analog_input(volt, channel = 114)
            lpp.add_gps(0, 0, 55)
            lpp.send()
            time.sleep(0.1)
            #print('Data sent:')
        s.setblocking(False)
        time.sleep(0.1)
    else:
        pycom.rgbled(0x111111)
        #print("SLEEP MODE ACTIVATED . . .")
        time.sleep(0.2)
        #py.setup_sleep(20)
        #py.go_to_sleep()
        print(". . .")
        #ds.go_to_sleep(10)
    gc.mem_free() #Clean the memory
