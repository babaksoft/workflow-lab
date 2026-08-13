"""
Application-wide settings.
"""

import logging
import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

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


def load_environment() -> None:
    """
    Load all environment variables from .env file.
    """

    load_dotenv(find_dotenv())
