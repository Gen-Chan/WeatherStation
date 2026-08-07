# Weather Station
A weather station made with a Raspberry Nano and a BME280 or a BMP280 (I will talk about BME280 because I like humidity)

At first, I find a good base for my project. It was created by stfn a can be found [here](https://stfn.pl/blog/34-pico-power-consumption-solar-panels/)
After a lot of changes, it is what you can find in this repo.
The main feature of this script is to gather metrics via the BME 280 and send them to a prometheus instance via pushgateway
to power saving and run the system, a LiPo 3.7 2000mAh accu, I shut down the WiFi and only turn it on to upload the data.

## used Hardware
- Raspberry Pi Pico W
- GY-BME 280 Module
- Universal USB-C Chargingboard
- 3.7V LiPo-Accu 2000mAh Typ 103450
- Heating for the Chargingboard

## install
1. Install MicroPython on your Pico (i.e. using thonny or VS Code)
2. copy everything from the script folder to the board
3. change the config.py to your environment

## ToDo
- Create a custom case for a 3d printer
- Publish configs of pushgateway, prometheus and graphana