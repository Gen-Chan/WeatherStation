# Weather Station
A Weather station made with a Raspberry Nano and a BME280 or a BMP280 (I will talk about BME280 because I like humility)

At first, I find a good Base for my Project. It was created by stfn a can be found [here](https://stfn.pl/blog/34-pico-power-consumption-solar-panels/)
After alot of changes, it is what you can find in this repo.
The main feature of this script is to gather metrics via the BME 280 and send them to a prometheus instance via pushgateway
to power saving and run the system a LiPo 3.7 2000mAh accu, I shutdown the WiFi and only turn it on to upload the data.

## ToDo
- Create a cutsom case for a 3d printer
- publish configs of pushgateway, prometheus and graphana