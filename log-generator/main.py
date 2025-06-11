
from prometheus_client import start_http_server, Counter, Histogram
import logging
import random
import sys
import time

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

# Clear existing handlers and add our stdout handler
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(handler)

log_levels=[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]    # Set the logging level

sample_messages = [
    "DEBUG - Auth token validation skipped in development mode",
    "INFO - User [user_1234] successfully authenticated via OAuth",
    "WARNING - Retry attempt [2/3] for service `PaymentGateway` timed out",
    "ERROR - Failed to fetch user preferences from Redis: Connection refused",
    "CRITICAL - OutOfMemoryError in job scheduler: forcing graceful shutdown",
    "INFO - User [user_5678] logged in from IP 192.168.1.45 at 2025-06-07 18:22:14",
    "INFO - User [user_5678] logged out after session duration: 43m 12s",
    "DEBUG - Processed 2,345 records in 1.34 seconds using pipeline v2.1.0",
    "ERROR - Data ingestion pipeline failed at stage: `transform_users_batch`",
    "INFO - Microservice `OrderService` is up and running on port 8081",
    "INFO - Initiating shutdown sequence: draining connections and saving state...",
    "WARNING - Disk usage at 91% for volume `/var/lib/postgresql`, consider cleanup",
    "DEBUG - Cache miss for key: `user_profile:83927`, triggering fallback query",
    "INFO - Backup completed successfully: snapshot ID `bkp-20250607-1915`",
    "ERROR - External API rate limit exceeded (HTTP 429): pausing for 60s",
]

def log_generator():
    """
    Function to generate log messages at different levels.
    """
    while True:
        log_levl = random.choice(log_levels)  # Randomly select a log level
        message = random.choice(sample_messages)  # Randomly select a message
        logging.log(log_levl, message)  
        time.sleep(random.uniform(0.5, 2))
        # Increment the Prometheus counter for the log level
        LOG_COUNTER.labels(level=logging.getLevelName(log_levl)).inc()

if __name__ == "__main__":
    print("Starting log generator...")
    log_generato= log_generator()
