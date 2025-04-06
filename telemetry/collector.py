import time
import os
import sqlite3
import importlib
import logging
from datetime import datetime
import sys
import requests  # Add for API submission option

from config import DB_PATH, API_KEY, AM2320_BUS_NUMBER, AM2320_ADDRESS
from db.init import get_db_connection, initialize_db
from db.data import save_sensor_reading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('collector')

class SensorCollector:
    def __init__(self, db_path, interval=60, use_api=False, api_url="http://localhost:5000"):
        """
        Initialize the sensor collector
        
        Args:
            db_path: Path to the SQLite database
            interval: Collection interval in seconds
            use_api: Whether to use the API for submission (instead of direct DB access)
            api_url: Base URL for the API
        """
        self.db_path = db_path
        self.interval = interval
        self.sensors = {}
        self.running = False
        self.use_api = use_api
        self.api_url = api_url
        
        # Initialize database
        initialize_db(db_path)
        
        # Load registered sensors from database
        self._load_sensors()
    
    def _load_sensors(self):
        """Load registered sensors from the database"""
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        
        # Get active sensors
        cursor.execute('SELECT * FROM sensors WHERE active = 1')
        
        for row in cursor.fetchall():
            sensor_type = row[1]  # type column
            location = row[2]     # location column

            try:
                # Dynamically import the sensor module
                module_path = f"sensors.{sensor_type.lower()}"
                module = importlib.import_module(module_path)
                
                # Get the class with the same name as the sensor type
                sensor_class = getattr(module, sensor_type)
                
                # Initialize the sensor
                self.sensors[sensor_type] = {
                    'instance': self._instantiate_sensor(sensor_class, sensor_type),
                    'info': dict(zip([column[0] for column in cursor.description], row))
                }
                
                logger.info(f"Loaded sensor: {sensor_type} at location: {location}")
            except (ImportError, AttributeError) as e:
                logger.error(f"Failed to load sensor {sensor_type}: {e}")
        
        conn.close()
    
    def _instantiate_sensor(self, sensor_class, sensor_type):
        """Instantiate a sensor class with appropriate parameters"""
        # Use configuration based on sensor type
        if sensor_type == 'AM2320':
            return sensor_class(bus_number=AM2320_BUS_NUMBER, address=AM2320_ADDRESS)
        
        # Default instantiation
        return sensor_class()
    
    def save_data_via_api(self, sensor_type, data):
        """Save sensor data using the API endpoint"""
        try:
            api_data = {
                "sensor_type": sensor_type,
                **data
            }
            
            # Include API key in headers
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": API_KEY
            }
            
            # Send data to API
            response = requests.post(
                f"{self.api_url}/api/readings/submit", 
                json=api_data, 
                headers=headers
            )
            
            # Check for successful submission
            if response.status_code == 200:
                logger.info(f"Data submitted to API: {data}")
                return True
            else:
                logger.error(f"API submission failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error submitting to API: {e}")
            return False
    
    def collect_data(self):
        """Collect data from all sensors and save to database"""
        conn = None
        if not self.use_api:
            conn = get_db_connection(self.db_path)
        
        for sensor_type, sensor_info in self.sensors.items():
            try:
                sensor = sensor_info['instance']
                logger.info(f"Reading data from {sensor_type}")
                
                if sensor_type == 'AM2320':
                    temperature, humidity = sensor.read_data()
                    
                    if temperature is not None and humidity is not None:
                        data = {
                            'temperature': temperature,
                            'humidity': humidity
                        }
                        
                        # Save to database directly or via API
                        if self.use_api:
                            self.save_data_via_api(sensor_type, data)
                        else:
                            save_sensor_reading(conn, sensor_type, data)
                            logger.info(f"Saved reading: {data}")
                    else:
                        logger.warning(f"Failed to read data from {sensor_type}")
                
                # Add handlers for other sensor types here
                
            except Exception as e:
                logger.error(f"Error collecting data from {sensor_type}: {e}")
        
        if conn:
            conn.close()
    
    def start_collection(self):
        """Start the data collection loop"""
        self.running = True
        logger.info(f"Starting data collection, interval: {self.interval}s")
        logger.info(f"Using {'API' if self.use_api else 'direct DB access'} for data storage")
        
        try:
            while self.running:
                start_time = time.time()
                
                # Collect and save data
                self.collect_data()
                
                # Calculate sleep time to maintain consistent interval
                elapsed_time = time.time() - start_time
                sleep_time = max(0, self.interval - elapsed_time)
                
                if sleep_time > 0:
                    logger.debug(f"Sleeping for {sleep_time:.2f}s")
                    time.sleep(sleep_time)
                else:
                    logger.warning(f"Collection took longer than interval: {elapsed_time:.2f}s")
        
        except KeyboardInterrupt:
            logger.info("Collection stopped by user")
        finally:
            self.running = False
    
    def stop_collection(self):
        """Stop the data collection loop"""
        self.running = False
        logger.info("Stopping data collection")

def main():
    # Get collection interval from environment or use default
    interval = int(os.getenv("COLLECTION_INTERVAL", 60))
    
    # Determine if using API for submissions
    use_api = os.getenv("USE_API_SUBMISSION", "false").lower() == "true"
    api_url = os.getenv("API_URL", "http://localhost:5000")
    
    # Initialize collector
    collector = SensorCollector(DB_PATH, interval, use_api, api_url)
    
    # Start collection
    collector.start_collection()

if __name__ == "__main__":
    main() 