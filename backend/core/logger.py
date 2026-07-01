"""
Centralized logging configuration for the research agent.

Sets up consistent logging across all modules with timestamps and log levels.
"""

import logging
import os

# Get log level from environment variable (default: INFO)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Create application logger
logger = logging.getLogger("research-agent")