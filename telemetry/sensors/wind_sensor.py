import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1x15 import Mode

class WindSensor:
    def __init__(self, address=0x48):
        """Initialize the wind sensor using ADS1115 ADC.
        
        Args:
            address (int): I2C address of the ADS1115 (default: 0x48)
        """
        # Create the I2C bus
        self.i2c = busio.I2C(board.SCL, board.SDA)
        
        # Create the ADC object using the I2C bus
        self.ads = ADS.ADS1115(self.i2c, address=address)
        
        # Configure ADC for 5V range
        self.ads.gain = 1  # Set gain to 1 for ±4.096V range
        self.ads.mode = Mode.SINGLE  # Single-shot mode
        
        # Create single-ended input on channels
        self.direction_channel = AnalogIn(self.ads, ADS.P1)  # Wind direction
        self.speed_channel = AnalogIn(self.ads, ADS.P2)     # Wind speed
        
        # Wind sensor scaling factors
        self.DIRECTION_SCALE = 360.0 / 4.1  # degrees per volt
        self.SPEED_SCALE = 100.0 / 4.0      # m/s per volt
    
    def read_data(self):
        """Read wind speed and direction data from the sensor.
        
        Returns:
            tuple: (wind_speed, wind_direction, speed_voltage, direction_voltage) or (None, None, None, None) if reading fails
        """
        try:
            # Read wind sensor voltages
            direction_voltage = self.direction_channel.voltage
            speed_voltage = self.speed_channel.voltage
            
            # Convert to actual values
            wind_direction = direction_voltage * self.DIRECTION_SCALE
            wind_speed = speed_voltage * self.SPEED_SCALE
            
            return wind_speed, wind_direction, speed_voltage, direction_voltage
        except Exception as e:
            print(f"Error reading from wind sensor: {e}")
            return None, None, None, None

# Example usage
if __name__ == "__main__":
    sensor = WindSensor()
    wind_speed, wind_direction, speed_voltage, direction_voltage = sensor.read_data()
    
    if wind_speed is not None and wind_direction is not None:
        print(f"Wind Speed: {wind_speed:.1f} m/s (Raw: {speed_voltage:.3f}V)")
        print(f"Wind Direction: {wind_direction:.1f}° (Raw: {direction_voltage:.3f}V)")
    else:
        print("Failed to read sensor data") 