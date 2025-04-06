# Installation Guide

This guide covers different methods for installing the Windy Weather Telemetry System.

## Quick Install

The easiest way to install is using the provided script:

```bash
# Navigate to the project directory
cd windy/telemetry

# Make the script executable
chmod +x install.sh

# Run the installer (user mode, all components)
./install.sh
```

The install script supports several options:

```bash
# Install for all users (system-wide)
./install.sh --system

# Install only the collector component
./install.sh --collector

# Install only the API component
./install.sh --api

# Install system-wide, collector only
./install.sh --system --collector
```

## Manual Installation

If you prefer to install manually:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd windy/telemetry
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Copy the example environment file and adjust as needed:
   ```
   cp .env.example .env
   ```

4. Install as a system service (optional):
   ```
   # Install the full system (both collector and API)
   mkdir -p ~/.config/systemd/user/
   cp systemd/windy-telemetry.service ~/.config/systemd/user/
   systemctl --user daemon-reload
   systemctl --user enable windy-telemetry.service
   systemctl --user start windy-telemetry.service
   
   # Or, install only the collector
   cp systemd/windy-collector.service ~/.config/systemd/user/
   systemctl --user daemon-reload
   systemctl --user enable windy-collector.service
   systemctl --user start windy-collector.service
   
   # Or, install only the API server
   cp systemd/windy-api.service ~/.config/systemd/user/
   systemctl --user daemon-reload
   systemctl --user enable windy-api.service
   systemctl --user start windy-api.service
   ```

## System Requirements

- Python 3.7 or higher
- SQLite 3
- For the AM2320 sensor: I2C interface enabled on your device
- Network connectivity for API access

## Systemd Service Management

### Check Service Status

```
systemctl --user status windy-telemetry.service
```

### View Service Logs

```
journalctl --user -u windy-telemetry.service -f
```

### Restart Service

```
systemctl --user restart windy-telemetry.service
```

### Stop Service

```
systemctl --user stop windy-telemetry.service
```

## Troubleshooting

### Database Initialization Issues

If you encounter database errors, check:
- The data directory exists and is writable
- SQLite is installed
- The DB_PATH in your .env file is correct

### Sensor Connection Issues

If sensor readings fail:
- Verify I2C is enabled on your device
- Check the sensor address (AM2320_ADDRESS in .env)
- Verify the sensor is properly connected

### Service Not Starting

If the service fails to start:
- Check logs with `journalctl --user -u windy-telemetry.service`
- Verify the path to Python in the service file matches your installation
- Make sure all dependencies are installed correctly 