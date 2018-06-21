# fipy-GPS-Accelerometer-LoRa

Project Purpose:
Read GPS and Accelerometer values and push them to server via LoRa.

Hardwares that used:
FiPy, PyTrack, Multitech Conduit Gateway

-No payload decoder is required for this project because I used cayenneLPP library;
cayenneLPP is using for send the data to TTN network. It is easy because, just one click is enough for the decode hex code thanks to cayenneLPP.
Just select the option Payload Formats>>Cayenne and decode automatically.

It uses EU868 MHz standarts.

![cayenne-lpp dashboard](https://i.hizliresim.com/X6JgG6.png)
