import time
import am2320sensor

i = 1
while True:
	temperature = am2320sensor.ReadTemperature()
	humidity = am2320sensor.ReadHumidity()
	print(i, "Temperature:", temperature, "°C")
	print("Humidity:", humidity, "%RH\n")
	i = i + 1
	time.sleep(5)