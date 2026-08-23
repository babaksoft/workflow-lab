"""
API routes that handle HTTP requests to API endpoints.
"""

from workflow_lab.api.routes.health import router as health_router
from workflow_lab.api.routes.metrics import router as metrics_router
from workflow_lab.api.routes.workflow import router as workflow_router

__all__ = [
    "health_router",
    "metrics_router",
    "workflow_router",
]
