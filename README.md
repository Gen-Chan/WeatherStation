# Weather Station
A weather station made with a Raspberry Nano and a BME280 or a BMP280 (I will talk about BME280 because I like humidity)

At first, I find a good base for my project. It was created by stfn a can be found [here](https://stfn.pl/blog/34-pico-power-consumption-solar-panels/)
After a lot of changes, it is what you can find in this repo.
The main feature of this script is to gather metrics via the BME 280 and send them to a prometheus instance via pushgateway
to power saving and run the system, a LiPo 3.7 2000mAh accu, I shut down the WiFi and only turn it on to upload the data.

## ToDo
- Create a custom case for a 3d printer
- Publish configs of pushgateway, prometheus and graphana