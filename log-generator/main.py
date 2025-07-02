
from prometheus_client import start_http_server, Counter, Histogram
import logging
import random
import sys
import time
import sqlite3
from datetime import datetime


#defining metrics for prometheus
# --- Define metrics ---
# Metrics
LOG_COUNTER = Counter("snitchboard_logs_total", "Total logs emitted", ["level"])

# --- Start Prometheus metrics server on port 8000 ---
start_http_server(8001)
  
# Configure logging to stdout
logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

#Db path
db_path = '/Users/surabhip./Documents/Documents - Surabhi’s Mac mini/snitchboard_db.db'

# Clear existing handlers and add our stdout handler
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(handler)

log_levels=[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]    # Set the logging level



sample_messages = [
    "Auth token validation skipped in development mode",
    "User [user_1234] successfully authenticated via OAuth",
    "Retry attempt [2/3] for service `PaymentGateway` timed out",
    "Failed to fetch user preferences from Redis: Connection refused",
    "OutOfMemoryError in job scheduler: forcing graceful shutdown",
    "User [user_5678] logged in from IP 192.168.1.45 at 2025-06-07 18:22:14",
    "User [user_5678] logged out after session duration: 43m 12s",
    "Processed 2,345 records in 1.34 seconds using pipeline v2.1.0",
    "Data ingestion pipeline failed at stage: `transform_users_batch`",
    "Microservice `OrderService` is up and running on port 8081",
    "Initiating shutdown sequence: draining connections and saving state...",
    "Disk usage at 91% for volume `/var/lib/postgresql`, consider cleanup",
    "Cache miss for key: `user_profile:83927`, triggering fallback query",
    "Backup completed successfully: snapshot ID `bkp-20250607-1915`",
    "External API rate limit exceeded (HTTP 429): pausing for 60s",
]

def dbConnection():
    """
    Function to connect to SQLite database and create a table if it doesn't exist.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print("Connected to SQLite database.")
    cursor.execute('SELECT * from INGESTED_LOG')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.commit()
    conn.close()
    return conn, cursor

def emit( levelname, record: logging.LogRecord) -> None:
    # Extract details from the log record
    timestamp = datetime.utcnow().isoformat()   # Use UTC for consistency
    severity = levelname                # e.g., INFO, ERROR
    message = record              # Actual log message
    source = "FAST_API_SELF"                       # Logger name (like "__main__")

    # Connect to DB and insert
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO INGESTED_LOG (timestamp, severity, message, source)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, severity, message, source))
    conn.commit()
    conn.close()

def log_generator():
    """
    Function to generate log messages at different levels.
    """
    try:
        dbConnection()
        while True:
            log_levl = random.choice(log_levels)  # Randomly select a log level
            message = random.choice(sample_messages)  # Randomly select a message
            emit( log_levl, message)
            logging.log(log_levl, message)  
            time.sleep(random.uniform(0.5, 2))
            # Increment the Prometheus counter for the log level
            LOG_COUNTER.labels(level=logging.getLevelName(log_levl)).inc()
            dbConnection()
    except KeyboardInterrupt:
        
        print("Log generation stopped.")

if __name__ == "__main__":
    print("Starting log generator...")
    log_generato= log_generator()
