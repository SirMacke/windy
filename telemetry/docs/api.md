# API Documentation

The Windy Weather Telemetry System provides a RESTful API for retrieving and submitting sensor data.

## Base URL

The API is accessible at:
```
http://[server-address]:[port]
```

By default, the port is 5000 (configurable in .env).

## Authentication

Protected endpoints require an API key, which can be provided in two ways:

### Via HTTP Header

```
X-API-Key: your_secret_api_key_here
```

### Via Query Parameter

```
?api_key=your_secret_api_key_here
```

## Endpoints

### Get Latest Readings

Retrieve the most recent sensor readings.

```
GET /api/readings/latest
```

#### Parameters

- `limit` (optional): Maximum number of readings to return (default: 10)
- `sensor_type` (optional): Filter by sensor type (e.g., "AM2320")

#### Example Request

```
GET /api/readings/latest?limit=5&sensor_type=AM2320
```

#### Example Response

```json
[
  {
    "id": 42,
    "sensor_type": "AM2320",
    "timestamp": "2023-04-06T15:30:45",
    "temperature": 22.5,
    "humidity": 48.3,
    "wind_direction": null,
    "wind_speed": null
  },
  {
    "id": 41,
    "sensor_type": "AM2320",
    "timestamp": "2023-04-06T15:29:45",
    "temperature": 22.4,
    "humidity": 48.2,
    "wind_direction": null,
    "wind_speed": null
  }
]
```

### Get Readings by Time Range

Retrieve readings within a specific time range.

```
GET /api/readings/range
```

#### Parameters

- `start` (required): Start timestamp (ISO format)
- `end` (required): End timestamp (ISO format)
- `sensor_type` (optional): Filter by sensor type

#### Example Request

```
GET /api/readings/range?start=2023-04-06T00:00:00&end=2023-04-06T23:59:59&sensor_type=AM2320
```

#### Example Response

```json
[
  {
    "id": 35,
    "sensor_type": "AM2320",
    "timestamp": "2023-04-06T12:00:45",
    "temperature": 21.5,
    "humidity": 47.3,
    "wind_direction": null,
    "wind_speed": null
  },
  {
    "id": 36,
    "sensor_type": "AM2320",
    "timestamp": "2023-04-06T12:01:45",
    "temperature": 21.6,
    "humidity": 47.4,
    "wind_direction": null,
    "wind_speed": null
  }
]
```

### Submit a Reading (Protected)

Submit a new sensor reading. This endpoint requires API key authentication.

```
POST /api/readings/submit
```

#### Headers

```
Content-Type: application/json
X-API-Key: your_secret_api_key_here
```

#### Request Body

```json
{
  "sensor_type": "AM2320",
  "temperature": 25.2,
  "humidity": 60.5
}
```

#### Example Response

```json
{
  "success": true,
  "reading_id": 43
}
```

#### Error Response

```json
{
  "error": "Unauthorized. Valid API key required."
}
```

### List Sensors

List all registered sensors in the system.

```
GET /api/sensors
```

#### Example Response

```json
[
  {
    "id": 1,
    "type": "AM2320",
    "location": "Indoor",
    "active": 1,
    "added_at": "2023-04-05T14:25:33"
  }
]
```

### Health Check

Basic health check endpoint.

```
GET /api/health
```

#### Example Response

```json
{
  "status": "healthy",
  "timestamp": "2023-04-06T15:45:22"
}
```

## Error Handling

The API returns standard HTTP status codes:

- 200: Success
- 400: Bad Request (e.g., missing required parameters)
- 401: Unauthorized (invalid or missing API key)
- 404: Not Found
- 500: Server Error

Error responses include an "error" field with a description:

```json
{
  "error": "start and end parameters are required"
}
```

## Sample API Usage

### Python

```python
import requests
import json

# Configuration
API_URL = "http://localhost:5000"
API_KEY = "your_secret_api_key_here"

# Get latest readings
response = requests.get(f"{API_URL}/api/readings/latest?limit=5")
readings = response.json()
print(json.dumps(readings, indent=2))

# Submit a new reading
headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}
data = {
    "sensor_type": "AM2320",
    "temperature": 25.2,
    "humidity": 60.5
}
response = requests.post(f"{API_URL}/api/readings/submit", 
                        json=data, 
                        headers=headers)
result = response.json()
print(json.dumps(result, indent=2))
```

### JavaScript

```javascript
// Get latest readings
fetch('http://localhost:5000/api/readings/latest?limit=5')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

// Submit a new reading
fetch('http://localhost:5000/api/readings/submit', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'your_secret_api_key_here'
  },
  body: JSON.stringify({
    sensor_type: 'AM2320',
    temperature: 25.2,
    humidity: 60.5
  })
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
``` 