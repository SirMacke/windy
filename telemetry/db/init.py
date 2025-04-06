import sqlite3
import os
from pathlib import Path
from config import AM2320_ENABLED, AM2320_LOCATION

def initialize_db(db_path):
    """Initialize the SQLite database with the required tables"""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create sensor_readings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_type TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        temperature REAL,
        humidity REAL,
        wind_direction TEXT,
        wind_speed REAL
    )
    ''')
    
    # Create sensors table to track available sensors
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL UNIQUE,
        location TEXT,
        active BOOLEAN DEFAULT 1,
        added_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Insert the AM2320 sensor if not exists
    if AM2320_ENABLED:
        cursor.execute('''
        INSERT OR IGNORE INTO sensors (type, location, active)
        VALUES (?, ?, ?)
        ''', ('AM2320', AM2320_LOCATION, True))
    else:
        # Update existing sensor to inactive if disabled
        cursor.execute('''
        UPDATE sensors SET active = 0 WHERE type = 'AM2320'
        ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    return True

def get_db_connection(db_path):
    """Get a connection to the SQLite database"""
    # Ensure the database is initialized
    if not os.path.exists(db_path):
        initialize_db(db_path)
    
    return sqlite3.connect(db_path) 