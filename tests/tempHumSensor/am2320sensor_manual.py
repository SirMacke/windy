import smbus
import time
i2cbus = 1 #Default
address = 0x5C #AM2020 I2C Address
bus = smbus.SMBus(i2cbus)

def WakeSensor():
	while True:
		try:
			bus.write_i2c_block_data(address, 0x00, [])
			break
		except IOError:
			pass
	time.sleep(0.003)

def ReadTemperature():
	WakeSensor()
	while True:
		try:
			bus.write_i2c_block_data(address, 0x03, [0x02, 0x02])
			break
		except IOError:
			pass
		time.sleep(0.015)

		try:
			block = bus.read_i2c_block_data(address, 0, 4)
		except IOError:
			pass

	temperature = float(block[2] << 8 | block[3]) / 10
	return temperature

def ReadHumidity():
	WakeSensor()
	while True:
		try:
			bus.write_i2c_block_data(address, 0x03, [0x00, 0x02])
			break
		except IOError:
			pass
	time.sleep(0.015)

	try:
		block = bus.read_i2c_block_data(address, 0, 4)
	except IOError:
		pass

	humidity = float(block[2] << 8 | block[3]) / 10
	return humidity

def ReadTemperatureHumidity():
	WakeSensor()
	while True:
		try:
			bus.write_i2c_block_data(address, 0x03, [0x00, 0x04])
			break
		except IOError:
			pass
	time.sleep(0.015)

	try:
		block = bus.read_i2c_block_data(address, 0, 6)
	except IOError:
		pass

	humidity = float(block[2] << 8 | block[3]) / 10
	temperature = float(block[4] << 8 | block[5]) / 10
	return temperature, humidity

i = 1
while True:
	temperature = ReadTemperature()
	humidity = ReadHumidity()
	print(i, "Temperature:", temperature, "°C")
	print("Humidity:", humidity, "%RH\n")
	i = i + 1
	time.sleep(5)