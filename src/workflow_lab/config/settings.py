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


def _load_docker_secrets() -> None:
    secret_mapping = {
        "/run/secrets/openai_api_key": "OPENAI_API_KEY",
        "/run/secrets/bedrock_api_key": "AWS_BEARER_TOKEN_BEDROCK",
    }

    for path, environment_variable in secret_mapping.items():
        secret_path = Path(path)

        if secret_path.exists():
            os.environ[environment_variable] = secret_path.read_text().strip()


_load_environment()
_load_docker_secrets()

# Global settings
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
PKG_ROOT = Path(__file__).resolve().parent.parent

# Log settings
LOCAL_LOG_DIR = REPO_ROOT / "logs"
LOG_DIR = Path(os.getenv("LOG_DIR", str(LOCAL_LOG_DIR)))

LOG_FILE = LOG_DIR / "workflow_lab.log"
LOG_LEVEL = logging.DEBUG

# LLM settings (Dev mode only, Environment: WSL NAT)
OLLAMA_BASE_URL = "http://172.31.80.1:11434"

# API settings
API_URL_PREFIX = "/api/v1"
LOCAL_URL_PREFIX = f"http://localhost:8000{API_URL_PREFIX}"
URL_PREFIX = os.getenv("URL_PREFIX", LOCAL_URL_PREFIX)

# Phoenix settings
PHOENIX_ENABLED = os.getenv("PHOENIX_ENABLED", "false").lower() == "true"

LOCAL_PHOENIX_PROJECT_NAME = "workflow-lab-dev"
PHOENIX_PROJECT_NAME = os.getenv(
    "PHOENIX_PROJECT_NAME",
    LOCAL_PHOENIX_PROJECT_NAME,
)

LOCAL_PHOENIX_COLLECTOR_ENDPOINT = "http://127.0.0.1:6006/v1/traces"
PHOENIX_COLLECTOR_ENDPOINT = os.getenv(
    "PHOENIX_COLLECTOR_ENDPOINT",
    LOCAL_PHOENIX_COLLECTOR_ENDPOINT,
)
