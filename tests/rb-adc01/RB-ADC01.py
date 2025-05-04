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
ads.gain = 2/3  # Set gain to 2/3 for ±6.144V range (16-bit ADC = 65536 steps over 12.288V total range)
#ads.gain = 1  # Set gain to 1 for ±4.096V range (16-bit ADC = 65536 steps over 8.192V total range)
                # This gives ~0.125mV resolution (8.192V/65536)a
#ads.gain = 4
ads.mode = Mode.SINGLE  # Single-shot mode
#ads.mode = Mode.CONTINUOUS  # Continuous measurement mode for real-time wind monitoring - does not work


# Create single-ended input for temperature
#chan0 = AnalogIn(ads, ADS.P0)  # Temperature

# Create single-ended input on channels
#chan1 = AnalogIn(ads, ADS.P1)  # Wind direction
#chan2 = AnalogIn(ads, ADS.P2)  # Wind speed

# Create differential inputs for wind sensors
# For wind direction, connect positive to P0 and negative to P1
chan_dir = AnalogIn(ads, ADS.P0, ADS.P1)  # Wind direction (differential)

# For wind speed, connect positive to P2 and negative to P3
chan_speed = AnalogIn(ads, ADS.P2, ADS.P3)  # Wind speed (differential)

# Temperature sensor constants
Tn = 298.15  # Reference temperature in Kelvin (25°C)
B = 3980     # B-value of the NTC thermistor
Rn = 10000   # Reference resistance at Tn

# Wind sensor scaling factors
# Adjust these values based on your sensor specifications
DIRECTION_SCALE = 360.0 / 5.0  # degrees per volt
SPEED_SCALE = 100.0 / 4.0      # m/s per volt

while True:
    # Read temperature
    #ntc = chan0.voltage
    #Rt = (10000 / ntc) * (3.3 - ntc) - 10000
    #temp = (1 / ((1/Tn) + (1/B) * math.log(Rt / Rn))) - 273.15
    temp = 0
    
    # Read wind sensor voltages
    #direction_voltage = chan1.voltage
    #speed_voltage = chan2.voltage
    direction_voltage = chan_dir.voltage
    speed_voltage = chan_speed.voltage
    
    # Convert to actual values
    #wind_direction = direction_voltage * DIRECTION_SCALE
    #wind_speed = speed_voltage * SPEED_SCALE

    # For differential readings, voltage could be negative
    # Adjust the calculation based on your sensor's specifications
    # Simple direction calculation - similar to speed calculation
    # Offset by 0.046V (the reading when no wind) and scale appropriately
    direction_offset = 0.047  # Voltage when no wind
    wind_direction = min(360, max(0, (abs(direction_voltage) - direction_offset) * DIRECTION_SCALE))
    
    # For differential speed readings
    speed_offset = 0.002  # Voltage when no wind
    wind_speed = max(0, (abs(speed_voltage) - speed_offset) * SPEED_SCALE)  # Use absolute value as speed is always positive
    
    print("Temp:      {:>5.1f}°C".format(temp))
    print("Direction: {:>5.1f}° ({:>5.3f}V, raw: {:>5d})".format(wind_direction, direction_voltage, chan_dir.value))
    print("Speed:     {:>5.1f}m/s ({:>5.3f}V, raw: {:>5d})".format(wind_speed, speed_voltage, chan_speed.value))
    
    # Determine voltage limit based on gain
    if ads.gain == 1:
        v_limit = 4.096
    elif ads.gain == 2/3:
        v_limit = 6.144
    else:
        v_limit = 4.096
    
    if any(v > (v_limit * 0.98) for v in [abs(direction_voltage), abs(speed_voltage)]):
        print("WARNING: Near {:.3f}V limit!".format(v_limit))
    print("-------------------")
    time.sleep(1)
