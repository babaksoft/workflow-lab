"""
Application-wide settings.
"""

import logging
import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv


def _load_environment() -> None:
    """
    Load all environment variables from .env file.

    Not meant to be called from outside this module.
    """

    load_dotenv(find_dotenv())


_load_environment()

# Global settings
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
PKG_ROOT = Path(__file__).resolve().parent.parent

# Log settings
LOG_DIR = REPO_ROOT / "logs"
LOG_FILE = LOG_DIR / "workflow_lab.log"
LOG_LEVEL = logging.DEBUG

# API settings
LOCAL_URL_PREFIX = "http://127.0.0.1:8000/api/v1"
URL_PREFIX = os.getenv("URL_PREFIX", LOCAL_URL_PREFIX)

# Phoenix settings
PHOENIX_ENABLED = os.getenv("PHOENIX_ENABLED", "false").lower() == "true"

LOCAL_PHOENIX_PROJECT_NAME = "workflow-lab-dev"
PHOENIX_PROJECT_NAME = os.getenv(
    "PHOENIX_PROJECT_NAME",
    LOCAL_PHOENIX_PROJECT_NAME,
)

LOCAL_PHOENIX_COLLECTOR_ENDPOINT = "http://127.0.0.1:6006"
PHOENIX_COLLECTOR_ENDPOINT = os.getenv(
    "PHOENIX_COLLECTOR_ENDPOINT",
    LOCAL_PHOENIX_COLLECTOR_ENDPOINT,
)
