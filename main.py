# Copyright by stfn
# https://stfn.pl/blog/34-pico-power-consumption-solar-panels/
#
# some customizations by myself, Gen-Chan
# to let it suite my requierments.
# Core idea is a machine that gather weather metrics and write them
# to a prometheus datastorage and visualisati them with grafana

#import json
from time import sleep

import bme280
import machine
import network
#from umqtt.simple import MQTTClient

sdaPIN = machine.Pin(0)
sclPIN = machine.Pin(1)

i2c = machine.I2C(0, sda=sdaPIN, scl=sclPIN)
bme = bme280.BME280(i2c=i2c)

led = machine.Pin("LED", machine.Pin.OUT)

ssid = "wlan.Gen-Chan-2"
password = "1Klavier"

while True:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    max_wait = 30
    while max_wait > 0:
        if wlan.isconnected():
            break
        max_wait -= 1
        sleep(1)

    if not wlan.isconnected():
        machine.reset()

    led.on()
    sleep(0.2)
    led.off()
    data = bme.read_compensated_data()
    payload = {
        "temperature": data[0] / 100,
        "pressure": data[1] / 256 / 100,
        "humidity": data[2] / 1024,
    }

    print(payload)

    wlan.active(False)
    wlan.deinit()
    sleep(300)
