from typing import Any

from pydantic import BaseModel, Field


class WorkflowResponse(BaseModel):
    """
    Represents the response returned by a workflow execution.

    Attributes:
        result:
            Result produced by the workflow.
    """

    result: dict[str, Any] = Field(
        ...,
        description="Result produced by the workflow.",
    )
