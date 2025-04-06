import sqlite3
from datetime import datetime

def save_sensor_reading(conn, sensor_type, data):
    """
    Save sensor reading to the database
    
    Args:
        conn: SQLite connection
        sensor_type: Type of sensor (e.g., 'AM2320')
        data: Dictionary containing sensor data (temperature, humidity, etc.)
    
    Returns:
        ID of the inserted record
    """
    cursor = conn.cursor()
    
    # Extract values from data dictionary, use None for missing values
    values = {
        'sensor_type': sensor_type,
        'temperature': data.get('temperature'),
        'humidity': data.get('humidity'),
        'wind_direction': data.get('wind_direction'),
        'wind_speed': data.get('wind_speed')
    }
    
    # Build dynamic query based on available data
    fields = ['sensor_type']
    placeholders = ['?']
    query_values = [sensor_type]
    
    for key, value in values.items():
        if key != 'sensor_type' and value is not None:
            fields.append(key)
            placeholders.append('?')
            query_values.append(value)
    
    query = f'''
    INSERT INTO sensor_readings ({', '.join(fields)})
    VALUES ({', '.join(placeholders)})
    '''
    
    cursor.execute(query, query_values)
    conn.commit()
    
    return cursor.lastrowid

def get_latest_readings(conn, limit=10, sensor_type=None):
    """
    Get the latest readings from the database
    
    Args:
        conn: SQLite connection
        limit: Maximum number of readings to return
        sensor_type: Optional filter by sensor type
    
    Returns:
        List of readings
    """
    cursor = conn.cursor()
    
    query = '''
    SELECT * FROM sensor_readings 
    '''
    
    params = []
    if sensor_type:
        query += ' WHERE sensor_type = ? '
        params.append(sensor_type)
    
    query += ' ORDER BY timestamp DESC LIMIT ? '
    params.append(limit)
    
    cursor.execute(query, params)
    
    # Get column names
    columns = [description[0] for description in cursor.description]
    
    # Return results as list of dictionaries
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    
    return results

def get_readings_by_timerange(conn, start_time, end_time, sensor_type=None):
    """
    Get readings within a specific time range
    
    Args:
        conn: SQLite connection
        start_time: Start timestamp
        end_time: End timestamp
        sensor_type: Optional filter by sensor type
    
    Returns:
        List of readings
    """
    cursor = conn.cursor()
    
    query = '''
    SELECT * FROM sensor_readings 
    WHERE timestamp BETWEEN ? AND ?
    '''
    
    params = [start_time, end_time]
    if sensor_type:
        query += ' AND sensor_type = ? '
        params.append(sensor_type)
    
    query += ' ORDER BY timestamp ASC'
    
    cursor.execute(query, params)
    
    # Get column names
    columns = [description[0] for description in cursor.description]
    
    # Return results as list of dictionaries
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    
    return results 