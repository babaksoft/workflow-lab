"""
Request/Response schemas exposed and consumed by the API.
"""

from workflow_lab.api.schemas.health import HealthResponse
from workflow_lab.api.schemas.workflow import WorkflowResponse

__all__ = [
    "HealthResponse",
    "WorkflowResponse",
]
