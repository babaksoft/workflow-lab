import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from workflow_lab.config.logging import configure_logging
from workflow_lab.utils.instrumentation import instrument

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown lifecycle events.

    Args:
        app:
            FastAPI application instance.
    """

    configure_logging()

    if app.state.phoenix_enabled:
        instrument()

    logger.info("Starting Workflow Lab API")

    yield
