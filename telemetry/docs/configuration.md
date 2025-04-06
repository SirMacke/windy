# Configuration Guide

This guide covers how to configure the Windy Weather Telemetry System to suit your needs.

## Environment Variables

The system is configured through environment variables, which can be set in the `.env` file. The installer creates this file automatically, or you can copy it from `.env.example`.

Here's a breakdown of all available configuration options:

```
# Database configuration
DB_PATH=./data/windy.db

# Sensor configuration
AM2320_ADDRESS=0x5C

# Collection configuration
COLLECTION_INTERVAL=60

# API security
API_KEY=your_secret_api_key_here
REQUIRE_API_KEY=true

# API submission (for distributed sensors)
USE_API_SUBMISSION=false
API_URL=http://localhost:5000

# Flask API configuration
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_APP=api.py
FLASK_RUN_PORT=5000
FLASK_RUN_HOST=0.0.0.0
```

## Database Configuration

- `DB_PATH`: Path to the SQLite database file
  - Default: `./data/windy.db`
  - You can use an absolute path if needed

## Sensor Configuration

- `AM2320_ADDRESS`: I2C address of the AM2320 temperature/humidity sensor
  - Default: `0x5C` (standard address for this sensor)
  - Only change if your sensor has a different address

## Collection Configuration

- `COLLECTION_INTERVAL`: How often to collect sensor data (in seconds)
  - Default: `60` (once per minute)
  - Lower values increase database size but provide more detailed data
  - Recommended range: 30-300 seconds

## API Security

- `API_KEY`: Secret key for authenticating API requests
  - Generated randomly during installation if not specified
  - Should be kept secret and secure
  - Used for submitting sensor data via the API

- `REQUIRE_API_KEY`: Whether to require API key authentication
  - Default: `true`
  - Set to `false` only in secure, isolated networks
  - Not recommended for public deployments

## Distributed Sensor Configuration

For setups where sensors are on different devices than the main database:

- `USE_API_SUBMISSION`: Whether to use the API for data submission
  - Default: `false` (direct database access)
  - Set to `true` on remote sensor devices

- `API_URL`: URL of the API server
  - Default: `http://localhost:5000`
  - Change to the actual server address for remote sensors

## Flask API Configuration

- `FLASK_ENV`: Flask environment (development or production)
  - Use `development` for debugging
  - Use `production` for deployment

- `FLASK_DEBUG`: Enable/disable Flask debug mode
  - Set to `0` for production

- `FLASK_APP`: Flask application entry point
  - Default: `api.py`
  - Don't change unless restructuring the application

- `FLASK_RUN_PORT`: Port for the Flask API server
  - Default: `5000`
  - Change if port conflicts exist

- `FLASK_RUN_HOST`: Host interface for the Flask API server
  - Default: `0.0.0.0` (all interfaces)
  - Set to `127.0.0.1` for local-only access

## Command Line Options

You can override some configuration options via command line arguments:

```bash
# Run with a different collection interval (30 seconds)
python index.py --interval 30

# Run only the API server
python index.py --api-only

# Run only the data collector
python index.py --collector-only
```

## Distributed Deployment Configuration

For a distributed setup with multiple sensors feeding to a central server:

### Central Server

```
# Database and API configuration
DB_PATH=/path/to/database.db
API_KEY=shared_secret_key
REQUIRE_API_KEY=true
FLASK_RUN_HOST=0.0.0.0  # Listen on all interfaces
```

### Remote Sensor Nodes

```
# Sensor node configuration
USE_API_SUBMISSION=true
API_URL=http://central-server-ip:5000
API_KEY=shared_secret_key  # Same as central server
``` 