# Auto-generated file
from loguru import logger
import sys
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger.remove()

#console logging
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO"
)

# file logging
logger.add(
    f"{LOG_DIR}/app.log",
    rotation="10 mb",
    retention="7 days",
    compression="zip",
    level="INFO"
)
