# System Architecture

This document describes the architecture of the Windy Weather Telemetry System.

## Overview

The system follows a modular design with clear separation of concerns:

- **Data Collection**: Gathering sensor data at defined intervals
- **Data Storage**: Persisting data in a SQLite database
- **Data Access**: Retrieving data via a RESTful API

## System Components

![System Architecture](../assets/architecture.png)

### Core Components

1. **Sensors Module**
   - Abstractions for physical sensor hardware
   - Independent modules for each sensor type
   - Common interface for data collection

2. **Data Collector**
   - Periodic data collection from sensors
   - Extensible for different sensor types
   - Direct database storage or API submission

3. **Database Module**
   - Schema initialization and management
   - Data access layer
   - Query utilities

4. **API Server**
   - RESTful endpoints for data access
   - API key authentication for protected endpoints
   - Decoupled from data collection

### Directory Structure

```
telemetry/
├── api.py             # Flask API implementation
├── collector.py       # Sensor data collection logic
├── config.py          # Configuration management
├── db/                # Database modules
│   ├── init.py        # Database initialization
│   └── data.py        # Data access functions
├── data/              # Database storage location
├── index.py           # Main entry point
├── install.sh         # Installation script
├── sensors/           # Sensor modules
│   └── am2320.py      # AM2320 temperature/humidity sensor
├── systemd/           # Systemd service files
├── .env               # Environment variables
└── requirements.txt   # Python dependencies
```

## Data Flow

1. **Sensor Reading**
   - Physical sensors capture environmental data
   - Sensor modules interface with hardware
   - Raw data is converted to appropriate units

2. **Data Collection**
   - Collector polls each active sensor at defined intervals
   - Raw sensor data is validated and formatted
   - Data is timestamped and prepared for storage

3. **Data Storage**
   - Formatted data is saved to SQLite database
   - Each reading includes sensor type and timestamp
   - Metadata about sensors is maintained

4. **Data Access**
   - API server provides access to stored data
   - Query parameters allow filtering and limiting results
   - JSON responses for easy integration

## Database Schema

### sensor_readings Table

Stores actual sensor readings:

```sql
CREATE TABLE sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_type TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperature REAL,
    humidity REAL,
    wind_direction TEXT
    wind_speed REAL,
)
```

### sensors Table

Tracks registered sensors:

```sql
CREATE TABLE sensors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL UNIQUE,
    location TEXT,
    active BOOLEAN DEFAULT 1,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

## Security Model

- **API Key Authentication**
  - Required for submitting sensor data
  - Optional for other endpoints (configurable)
  - Can be provided via HTTP headers or query parameters

- **Database Security**
  - File-based SQLite database
  - Protected by filesystem permissions
  - No direct network access to database

## Deployment Options

### Single Device Deployment

The entire system runs on a single device (e.g., Raspberry Pi):
- Sensors connected directly to the device
- Database stored locally
- API accessible via device's network interface

### Distributed Deployment

Components can be split across multiple devices:
- Central server hosts database and API
- Remote devices with sensors submit data via API
- API key authentication ensures data integrity

## Extensibility

The system is designed for easy extension:

1. **New Sensor Types**
   - Add new sensor modules in the `sensors/` directory
   - Update collector logic to handle the new sensor type
   - Register the sensor in the database

2. **Additional Data Points**
   - Database schema includes common weather data points
   - Easily extendable for new data types

3. **Alternative Data Storage**
   - Abstract data access layer allows changing storage
   - Could be extended to support other databases

## Performance Considerations

- **Data Volume**
  - With 1-minute collection intervals, a single sensor produces approximately:
    - 1,440 readings per day
    - 10,080 readings per week
    - ~43,800 readings per month
  - SQLite efficiently handles this volume for several years
  - Consider data retention policies for long-term use

- **Resource Usage**
  - CPU: Minimal (mainly during data collection and API requests)
  - Memory: Small footprint (~50MB typical)
  - Storage: ~10KB per day per sensor (typical)

## Limitations

- **Scaling**
  - SQLite may become a bottleneck with many concurrent API requests
  - Consider migrating to PostgreSQL or similar for larger deployments

- **Reliability**
  - Power outages can cause data loss (mitigate with UPS)
  - Network outages in distributed setups cause delayed data collection 