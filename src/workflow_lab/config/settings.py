"""
Application-wide settings that complement observability.
"""

import logging
from pathlib import Path

# Global settings
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
PKG_ROOT = Path(__file__).resolve().parent.parent

# Log settings
LOG_DIR = REPO_ROOT / "logs"
LOG_FILE = LOG_DIR / "workflow_lab.log"
LOG_LEVEL = logging.DEBUG
