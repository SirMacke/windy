import os
import sys
import time
import argparse
import logging
from multiprocessing import Process

from config import DB_PATH, COLLECTION_INTERVAL
from db.init import initialize_db
from collector import SensorCollector
import api

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('windy')

def start_collector(interval):
    """Start the data collector process"""
    collector = SensorCollector(DB_PATH, interval)
    collector.start_collection()

def start_api_server():
    """Start the Flask API server"""
    api.app.run(debug=True, host='0.0.0.0', port=5000)

def main():
    """Main entry point for the weather telemetry system"""
    parser = argparse.ArgumentParser(description='Windy Weather Telemetry System')
    parser.add_argument('--api-only', action='store_true', help='Run only the API server')
    parser.add_argument('--collector-only', action='store_true', help='Run only the data collector')
    parser.add_argument('--interval', type=int, default=COLLECTION_INTERVAL, 
                        help=f'Data collection interval in seconds (default: {COLLECTION_INTERVAL})')
    args = parser.parse_args()

    # Initialize the database
    try:
        initialize_db(DB_PATH)
        logger.info(f"Database initialized at {DB_PATH}")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return 1

    # Determine what components to run
    run_api = not args.collector_only
    run_collector = not args.api_only

    processes = []

    try:
        # Start the API server if requested
        if run_api:
            logger.info("Starting API server...")
            api_process = Process(target=start_api_server)
            api_process.start()
            processes.append(api_process)

        # Start the collector if requested
        if run_collector:
            logger.info(f"Starting data collector with interval {args.interval}s...")
            collector_process = Process(target=start_collector, args=(args.interval,))
            collector_process.start()
            processes.append(collector_process)

        # Keep the main process running
        while any(p.is_alive() for p in processes):
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        # Terminate all processes
        for p in processes:
            if p.is_alive():
                p.terminate()
                p.join()

    return 0

if __name__ == "__main__":
    sys.exit(main())
