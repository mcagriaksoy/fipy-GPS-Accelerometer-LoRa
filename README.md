# fipy-GPS-Accelerometer-LoRa

Project Purpose:
Read GPS and Accelerometer values and push them to server via LoRa.

Hardwares that used:
FiPy, PyTrack, Multitech Conduit Gateway

In this project, I pay attention to consume low power and stability. To decrease power consumption I used Cayenne LPP, Accelerometer sleep - wake up modes and close the unnecessary functions of FiPY.
Network:
TTN(The things network)
https://www.thethingsnetwork.org/

-No payload decoder is required for this project because I used cayenneLPP library. If I had used other scenerios, I would have required decode my message with payload decoder tab in the TTN. 

CayenneLPP is using for send the data to TTN network. It is easy because, just one click is enough for the decode hex code thanks to cayenneLPP.
Just select the option Payload Formats>>Cayenne and decode automatically.
Also In python side we need to add these functions into the codeblock:
```
lpp.add_accelerometer(xsum,ysum,zsum)

lpp.add_analog_input(abs(gtotal-1))

lpp.add_analog_input(volt, channel = 114)

lpp.add_gps(c0, c1, 55)

lpp.send()
```

![Cayenne](https://github.com/mcagriaksoy/fipy-GPS-Accelerometer-LoRa/blob/master/1.PNG)


On the other hand we need to set the settings of LoRa:
```
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868,adr=False, tx_retries=0, device_class=LoRa.CLASS_A)

-Required keys can be found on TTN network >> Applications >> Dashboard

dev_addr = struct.unpack(">l", binascii.unhexlify('********'))[0]

nwk_swkey = binascii.unhexlify('***************')

app_swkey = binascii.unhexlify('****************')

lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)

print ("LoRa Initialized")
```

![Project](https://github.com/mcagriaksoy/fipy-GPS-Accelerometer-LoRa/blob/master/2.jpg)
