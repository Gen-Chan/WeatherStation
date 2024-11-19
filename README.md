# WeatherStation
A Weathersation made with a Arduino Nano and a BME280

At first I find a good Base for my Project. It was created by stfn an can be fount [here](https://stfn.pl/blog/34-pico-power-consumption-solar-panels/)
After some changes it is what you can find in this repo.
Main feature of this script is to geather metrics via the BME 280 and send them to a prometheus instance via remote_write
to powersaving and run the system with 4 x 1.25v Accu Typ AA, I shut down the WiFi and only turn it on to uploade the data.
