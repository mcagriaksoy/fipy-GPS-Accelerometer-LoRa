<a href="https://github.com/mcagriaksoy/fipy-GPS-Accelerometer-LoRa" title="Go to GitHub repo"><img src="https://img.shields.io/static/v1?label=mcagriaksoy&message=fipy-GPS-Accelerometer-LoRa&color=blue&logo=github" alt="mcagriaksoy - fipy-GPS-Accelerometer-LoRa"></a>
<a href="https://github.com/mcagriaksoy/fipy-GPS-Accelerometer-LoRa/releases/"><img src="https://img.shields.io/github/tag/mcagriaksoy/fipy-GPS-Accelerometer-LoRa?include_prereleases=&sort=semver&color=blue" alt="GitHub tag"></a>
<a href="#license"><img src="https://img.shields.io/badge/License-MIT-blue" alt="License"></a>
<a href="https://github.com/mcagriaksoy/fipy-GPS-Accelerometer-LoRa/issues"><img src="https://img.shields.io/github/issues/mcagriaksoy/fipy-GPS-Accelerometer-LoRa" alt="issues - fipy-GPS-Accelerometer-LoRa"></a>
[![OS - Linux](https://img.shields.io/badge/OS-Linux-blue?logo=linux&logoColor=white)](https://www.linux.org/ "Go to Linux homepage")
[![Hosted with GH Pages](https://img.shields.io/badge/Hosted_with-GitHub_Pages-blue?logo=github&logoColor=white)](https://pages.github.com/ "Go to GitHub Pages homepage")
[![OS - Windows](https://img.shields.io/badge/OS-Windows-blue?logo=windows&logoColor=white)](https://www.microsoft.com/ "Go to Microsoft homepage")

Project Purpose:
Read GPS and Accelerometer values and push them to the server via LoRa.

Hardware that used:
FiPy, PyTrack, Multitech Conduit Gateway

In this project, I pay attention to consume low power and stability. To decrease power consumption I used Cayenne LPP, Accelerometer sleep - wake up modes and close the unnecessary functions of FiPY.
Network:
TTN(The things network)
https://www.thethingsnetwork.org/

-No payload decoder is required for this project because I used the cayenneLPP library. If I had used other scenarios, I would have required decode my message with the payload decoder tab in the TTN. 

CayenneLPP is using to send the data to the TTN network. It is easy because just one click is enough for the decode hex code thanks to cayenneLPP.
Just select the option Payload Formats>>Cayenne and decode automatically.
Also In python side, we need to add these functions into the code block:
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
