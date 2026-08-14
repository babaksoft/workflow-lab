from fastapi import FastAPI

from workflow_lab.api.instrument import instrument_http_request
from workflow_lab.api.lifespan import lifespan
from workflow_lab.api.routes.metrics import router as metrics_router
from workflow_lab.api.routes.workflow import router as workflow_router
from workflow_lab.config import settings


def create_app(*, phoenix_enabled: bool | None = None) -> FastAPI:
    """
    Create and configure the FastAPI application.

    Args:
        phoenix_enabled:
            Whether Phoenix instrumentation should be enabled.
            If omitted, the application configuration is used.

    Returns:
        Configured FastAPI application.
    """

    app = FastAPI(
        title="Workflow Lab",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.state.phoenix_enabled = (
        settings.PHOENIX_ENABLED if phoenix_enabled is None else phoenix_enabled
    )

    app.middleware("http")(instrument_http_request)

    app.include_router(workflow_router, prefix="/api/v1")
    app.include_router(metrics_router, prefix="/api/v1")

    return app


app = create_app()
