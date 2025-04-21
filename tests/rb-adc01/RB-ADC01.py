#!/usr/bin/python

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1x15 import Mode
import math

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Configure ADC for 5V range
ads.gain = 1  # Set gain to 1 for ±4.096V range
ads.mode = Mode.SINGLE  # Single-shot mode

# Create single-ended input on channels
chan0 = AnalogIn(ads, ADS.P0)  # Temperature
chan1 = AnalogIn(ads, ADS.P1)  # Wind direction
chan2 = AnalogIn(ads, ADS.P2)  # Wind speed

# Temperature sensor constants
Tn = 298.15  # Reference temperature in Kelvin (25°C)
B = 3980     # B-value of the NTC thermistor
Rn = 10000   # Reference resistance at Tn

# Wind sensor scaling factors
# Assuming 0-5V corresponds to 0-360 degrees for direction
# and 0-5V corresponds to 0-100 m/s for speed (adjust these values based on your sensor specs)
DIRECTION_SCALE = 360.0 / 4.1  # degrees per volt
SPEED_SCALE = 100.0 / 4.0      # m/s per volt

while True:
    # Read temperature
    ntc = chan0.voltage
    Rt = (10000 / ntc) * (3.3 - ntc) - 10000
    temp = (1 / ((1/Tn) + (1/B) * math.log(Rt / Rn))) - 273.15
    
    # Read wind sensor voltages
    direction_voltage = chan1.voltage
    speed_voltage = chan2.voltage
    
    # Convert to actual values
    wind_direction = direction_voltage * DIRECTION_SCALE
    wind_speed = speed_voltage * SPEED_SCALE
    
    print("Temperature: {:>5.1f}°C".format(temp))
    print("Wind Direction: {:>5.1f}°".format(wind_direction))
    print("Wind Speed: {:>5.1f} m/s".format(wind_speed))
    print("Raw Voltages:")
    print("  Temperature: {:>5.3f}V".format(ntc))
    print("  Direction: {:>5.3f}V".format(direction_voltage))
    print("  Speed: {:>5.3f}V".format(speed_voltage))
    print("---------------------------------------------------")
    time.sleep(1)
