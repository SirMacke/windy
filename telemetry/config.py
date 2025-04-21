from dotenv import load_dotenv
import os
import secrets

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "./data/windy.db")
COLLECTION_INTERVAL = int(os.getenv("COLLECTION_INTERVAL", 60))

# Sensor toggle and location settings
AM2320_ENABLED = os.getenv("AM2320_ENABLED", "true").lower() == "true"
AM2320_BUS_NUMBER = int(os.getenv("AM2320_BUS_NUMBER", 1))
AM2320_ADDRESS = int(os.getenv("AM2320_ADDRESS", "0x5C"), 16)
AM2320_LOCATION = os.getenv("AM2320_LOCATION", "Default Location")

# Wind sensor settings
WIND_SENSOR_ENABLED = os.getenv("WIND_SENSOR_ENABLED", "true").lower() == "true"
WIND_SENSOR_ADDRESS = int(os.getenv("WIND_SENSOR_ADDRESS", "0x48"), 16)
WIND_SENSOR_LOCATION = os.getenv("WIND_SENSOR_LOCATION", "Default Location")

# API security
API_KEY = os.getenv("API_KEY", secrets.token_hex(16))
REQUIRE_API_KEY = os.getenv("REQUIRE_API_KEY", "true").lower() == "true"
