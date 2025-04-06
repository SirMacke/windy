# Windy Weather Telemetry System

A modular weather telemetry system for collecting, storing, and serving sensor data.

## Features

- Collects temperature and humidity data from AM2320 sensor
- Stores data in SQLite database
- RESTful API for data retrieval and submission
- API key authentication for protected endpoints
- Easily extendable to support additional sensors
- Configuration via environment variables

## Documentation

- [Installation Guide](docs/installation.md) - Setup and installation instructions
- [Configuration Guide](docs/configuration.md) - Configuring the system
- [API Documentation](docs/api.md) - API endpoints and usage
- [System Architecture](docs/architecture.md) - System components and design

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd windy/telemetry

# Run the installer script
chmod +x install.sh
./install.sh

# Or install manually
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env

# Start the application
python index.py
```

## License

[MIT License](LICENSE)
