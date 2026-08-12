from pydantic import BaseModel


class WorkflowResponse(BaseModel):
    """
    Represents the response returned by a workflow execution.

    Attributes:
        result:
            Result produced by the workflow.
    """

    result: int
