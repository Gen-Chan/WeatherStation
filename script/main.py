from config import sclPin, sdaPin, interval, wlan_ssid, wlan_pass, auth_user, auth_pass, server_uri
from machine import Pin, I2C, ADC
from time import sleep, time_ns
from bme280 import *
import network
import urequests as requests
import ubinascii
import gc

if not server_uri.startswith("https://"):
    print("WARN: Connection is not secure. use https.")

conversionFactor = 3.3 / 65535

# init
led = Pin("LED", Pin.OUT)
wlan = network.WLAN(network.STA_IF)
temperatureSensor = ADC(4)
i2c=I2C(0, scl=sclPin, sda=sdaPin, freq=40000)
try:
    bme280 = BME280(i2c=i2c)
except OSError:
    print("Sensor not found")
    bme280 = None

# prepare communication with pushgateway
auth_str = f"{auth_user}:{auth_pass}"
b64_auth = ubinascii.b2a_base64(auth_str.encode()).decode().strip()
headers = {
    "Authorization": f"Basic {b64_auth}",
    "Content-Type": "text/plain"
}

# Pico core temperature
def readCore():
    temperature = temperatureSensor.read_u16() * conversionFactor
    output = 27 - (temperature - 0.706) / 0.001721
    return output

# Batterycapatity
class batteryManager:
    def __init__(self):
        # ADC für VSYS initialisieren (Pin 29)
        self.vsys_adc = ADC(Pin(29))

        # table for the discargecurve of a LiPo 3.7V
        self.dischargeCurve = [
            (4.20, 100),
            (4.10, 90),
            (3.97, 80),
            (3.87, 70),
            (3.79, 60),
            (3.75, 50),
            (3.72, 40),
            (3.70, 30),
            (3.67, 20),
            (3.62, 10),
            (3.55, 5),
            (3.20, 0)
        ]

    def _read_vsys_voltage(self):
        # starting the mesuring
        self.wlanPin = Pin(25, Pin.OUT)
        self.wlanPin.value(1)
        sleep(0.01)
        # multiple messurings for a avarage value
        samples = [self.vsys_adc.read_u16() for _ in range(10)]
        raw_average = sum(samples) / len(samples)

        self.wlanPin.init(Pin.IN)

        return raw_average * conversionFactor * 3

    def get_battery_info(self):
        # make the percentige
        voltage = self._read_vsys_voltage()reset()

        if voltage >= self.dischargeCurve[0][0]:
            return voltage, 100.0
        if voltage <= self.dischargeCurve[-1][0]:
            return voltage, 0.0

        # valures between the points in the table (linea)
        for i in range(len(self.dischargeCurve) - 1):
            v_high, p_high = self.dischargeCurve[i]
            v_low, p_low = self.dischargeCurve[i+1]

            if v_high >= voltage >= v_low:
                percentage = p_low + (voltage - v_low) * (p_high - p_low) / (v_high - v_low)
                return voltage, round(percentage, 1)

        return voltage, 0.0

battery = batteryManager()

while True:
    # geathering the data we want to submit. The sensordata might be interfere with wifi
    if bme280 is not None:
        try:
            weather = bme280.read_compensated_data()
            env_temp = weather[0] / 100
            env_press = weather[1] / 256 / 100
            env_hum = weather[2] / 1024
        except OSError:
            print("Error while reading sensor")
            env_temp, env_press, env_hum = 0.0, 0.0, 0.0
    else:
        env_temp, env_press, env_hum = 0.0, 0.0, 0.0

    volts, percent = battery.get_battery_info()
    sys_temp = readCore()

    payload = f"""env_temperature {env_temp}\n
env_pressure {env_press}\n
env_humidity {env_hum}\n
sys_temperature {sys_temp}\n
sys_batteryVolt {volts}\n
sys_batteryPercent {percent}\n"""


    wlan.active(True)
    wlan.connect(wlan_ssid, wlan_pass)
    max_wait = 30

    while max_wait > 0:
        if wlan.isconnected():
            led.on()
            break
        max_wait -= 1
        sleep(1)

    if not wlan.isconnected():
        led.off()
        print("WLAN no connection")
        continue


    try:
        response = requests.post(server_uri, data=payload, headers=headers, timeout=10)
        print("Status:", response.status_code)
        print("Response:", response.text)
        print("Payload:", payload)
        response.close()

    except Exception as e:
        print("Error:", e)

    try:
        wlan.disconnect()
    except:
        pass
    wlan.active(False)
    led.off()

    gc.collect()
    sleep(interval)
