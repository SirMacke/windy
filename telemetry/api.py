from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime
from functools import wraps

from config import DB_PATH, API_KEY, REQUIRE_API_KEY
from db.init import get_db_connection
from db.data import get_latest_readings, get_readings_by_timerange, save_sensor_reading

app = Flask(__name__)

# Helper function for database connection
def get_db():
    conn = get_db_connection(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

# Decorator to handle database connections
def with_db_connection(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        conn = get_db()
        try:
            result = f(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return decorated_function

# Decorator to require API key for protected endpoints
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not REQUIRE_API_KEY:
            return f(*args, **kwargs)
            
        # Check for API key in header or query parameters
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key or api_key != API_KEY:
            return jsonify({
                "error": "Unauthorized. Valid API key required."
            }), 401
            
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/readings/latest', methods=['GET'])
@with_db_connection
def latest_readings(conn):
    """Get the latest sensor readings"""
    limit = request.args.get('limit', 10, type=int)
    sensor_type = request.args.get('sensor_type')
    
    readings = get_latest_readings(conn, limit, sensor_type)
    return jsonify(readings)

@app.route('/api/readings/range', methods=['GET'])
@with_db_connection
def readings_by_range(conn):
    """Get readings within a date range"""
    start_time = request.args.get('start', type=str)
    end_time = request.args.get('end', type=str)
    sensor_type = request.args.get('sensor_type')
    
    if not start_time or not end_time:
        return jsonify({"error": "start and end parameters are required"}), 400
    
    readings = get_readings_by_timerange(conn, start_time, end_time, sensor_type)
    return jsonify(readings)

@app.route('/api/readings/submit', methods=['POST'])
@require_api_key
@with_db_connection
def submit_reading(conn):
    """Submit a new sensor reading (protected with API key)"""
    data = request.json
    
    if not data or 'sensor_type' not in data:
        return jsonify({"error": "sensor_type is required"}), 400
    
    sensor_type = data.pop('sensor_type')
    
    # Save the reading to the database
    reading_id = save_sensor_reading(conn, sensor_type, data)
    
    return jsonify({
        "success": True,
        "reading_id": reading_id
    })

@app.route('/api/sensors', methods=['GET'])
@with_db_connection
def list_sensors(conn):
    """List all registered sensors"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sensors WHERE active = 1')
    
    # Get column names
    columns = [description[0] for description in cursor.description]
    
    # Return results as list of dictionaries
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    
    return jsonify(results)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Basic health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000) 