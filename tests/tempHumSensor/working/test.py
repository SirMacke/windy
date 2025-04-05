import smbus
import time

bus = smbus.SMBus(1)
address = 0x5C

# Wake up the sensor
try:
    bus.write_byte(address, 0x00)
except:
    pass

time.sleep(0.1)

# Send read command
bus.write_i2c_block_data(address, 0x03, [0x00, 0x04])

time.sleep(0.05)

# Read data
data = bus.read_i2c_block_data(address, 0x00, 8)
print("Raw data:", data)

humidity = (data[2] << 8 | data[3]) / 10.0
temperature = (data[4] << 8 | data[5]) / 10.0

print(f"Temperature: {temperature}°C")
print(f"Humidity: {humidity}%")