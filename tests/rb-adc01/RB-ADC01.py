#!/usr/bin/python
# coding=utf-8

#############################################################################################################
### Copyright by Joy-IT
### Published under Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License
### Commercial use only after permission is requested and granted
###
### RB-ADC01 Analog Digital Converter - Raspberry Pi Python Code Example
###
#############################################################################################################
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import math

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channels
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

Tn = 298.15
B = 3980
Rn = 10000

while True:
    ntc = chan0.voltage
    Rt =  (10000 / ntc) * (3.3 - ntc) - 10000
    temp = (1 / ( (1/Tn) + (1/B) * math.log(Rt / Rn)) ) - 273.15
    print("temperature: ", "{:>5.2f} C".format(temp))
    print("channel 0: ","{:>5}\t{:>5.3f}".format(chan0.value, chan0.voltage))
    print("channel 1: ","{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage))
    print("channel 2: ","{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage))
    print("channel 3: ","{:>5}\t{:>5.3f}".format(chan3.value, chan3.voltage))
    print("---------------------------------------------------")
    time.sleep(1)
