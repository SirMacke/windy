import smbus
import time

class AM2320:
    def __init__(self, bus_number=1, address=0x5C):
        """Initialize the AM2320 sensor.
        
        Args:
            bus_number (int): I2C bus number (default: 1)
            address (int): I2C address of the sensor (default: 0x5C)
        """
        self.bus = smbus.SMBus(bus_number)
        self.address = address
    
    def wake_up(self):
        """Wake up the sensor by sending a command."""
        try:
            self.bus.write_byte(self.address, 0x00)
        except:
            pass
        time.sleep(0.1)
    
    def read_data(self):
        """Read temperature and humidity data from the sensor.
        
        Returns:
            tuple: (temperature, humidity) or (None, None) if reading fails
        """
        try:
            # Wake up the sensor
            self.wake_up()
            
            # Send read command
            self.bus.write_i2c_block_data(self.address, 0x03, [0x00, 0x04])
            time.sleep(0.05)
            
            # Read data
            data = self.bus.read_i2c_block_data(self.address, 0x00, 8)
            
            # Calculate temperature and humidity
            humidity = (data[2] << 8 | data[3]) / 10.0
            temperature = (data[4] << 8 | data[5]) / 10.0
            
            return temperature, humidity
        except Exception as e:
            print(f"Error reading from AM2320: {e}")
            return None, None
    
    def get_temperature(self):
        """Get only the temperature reading.
        
        Returns:
            float: Temperature in Celsius or None if reading fails
        """
        temperature, _ = self.read_data()
        return temperature
    
    def get_humidity(self):
        """Get only the humidity reading.
        
        Returns:
            float: Humidity percentage or None if reading fails
        """
        _, humidity = self.read_data()
        return humidity


# Example usage
if __name__ == "__main__":
    sensor = AM2320()
    temperature, humidity = sensor.read_data()
    
    if temperature is not None and humidity is not None:
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
    else:
        print("Failed to read sensor data")