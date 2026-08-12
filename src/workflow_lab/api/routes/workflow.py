from fastapi import APIRouter

from workflow_lab.api.instrument import (
    WORKFLOW_ERRORS,
    WORKFLOW_EXECUTIONS,
    WORKFLOW_LATENCY,
)
from workflow_lab.api.schemas.workflow import WorkflowResponse
from workflow_lab.utils.timer import Timer
from workflow_lab.workflows.math_flow import MathFlow

router = APIRouter(prefix="/workflow", tags=["workflow"])


@router.post("", response_model=WorkflowResponse)
async def run_workflow() -> WorkflowResponse:
    """
    Executes the math workflow.

    Returns:
        Workflow response containing the calculation result.

    Raises:
        Exception:
            If workflow execution fails.
    """

    workflow_name = "Simple Math"
    workflow = MathFlow(
        workflow_name=workflow_name,
        timeout=30,
        verbose=False,
    )

    with Timer() as timer:
        try:
            result = await workflow.run()
        except Exception:
            WORKFLOW_ERRORS.labels(workflow=workflow_name).inc()
            raise

    WORKFLOW_EXECUTIONS.labels(workflow=workflow_name).inc()

    WORKFLOW_LATENCY.labels(
        workflow=workflow_name,
    ).observe(timer.elapsed)

    return WorkflowResponse(result=result)
