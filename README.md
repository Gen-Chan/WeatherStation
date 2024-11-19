# Weather Station
A Weather station made with a Raspberry Nano and a BME280

At first, I find a good Base for my Project. It was created by stfn a can be found [here](https://stfn.pl/blog/34-pico-power-consumption-solar-panels/)
After some changes, it is what you can find in this repo.
The main feature of this script is to gather metrics via the BME 280 and send them to a prometheus instance via remote_write
to power saving and run the system with 4 x 1.25v accu type AA, I shut down the WiFi and only turn it on to upload the data.

## Files
main.py = Script for the Raspberry Nano
*.stl = 3D model that I use to put them on a wall.

## To do
add understanding remote_write and implement it
