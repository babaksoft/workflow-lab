from fastapi import APIRouter

from workflow_lab.api.schemas.workflow import WorkflowResponse
from workflow_lab.workflows.math_flow import MathFlow

router = APIRouter(prefix="/workflow", tags=["workflow"])


@router.post("", response_model=WorkflowResponse)
async def run_workflow() -> WorkflowResponse:
    """
    Executes the math workflow.

    Returns:
        Workflow response containing the calculation result.
    """

    workflow = MathFlow(workflow_name="Simple Math", timeout=30, verbose=False)
    result = await workflow.run()

    return WorkflowResponse(result=result)
