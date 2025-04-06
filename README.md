# Windy
A solar-powered Raspberry Pi Zero 2 weather station measuring wind direction, speed, temperature, and humidity with live web data.

## Software
- Telemetry script
- Nuxt website
- SQLite database
- Tests

## Hardware
### Raspberry Pi Zero 2 W
https://datasheets.raspberrypi.com/rpizero2/raspberry-pi-zero-2-w-product-brief.pdf
https://pinout.xyz/pinout/3v3_power

### Adafruit ASAIR AM2320
https://cdn-shop.adafruit.com/product-files/3721/AM2320.pdf
https://www.halvorsen.blog/documents/programming/python/resources/powerpoints/Raspberry%20Pi%20and%20AM2320%20Temperature%20and%20Humidity%20Sensor%20with%20I2C%20Interface.pdf
https://docs.circuitpython.org/projects/am2320/en/latest/index.html

Accuracy: +-3 %RH, +-0.5C

![AM2320 Temperature/Humidity Sensor Pinout](/images/image.png)

## Setup
1.
2.
3.
4.
5.
...

## Comments
onoff npm package doesn't work with node v22 due to epoll package


## Commands
sudo raspi-config

sudo apt-get install -y i2c-tools
sudo i2cdetect -y 1
sudo i2cget -y 1 0x5C