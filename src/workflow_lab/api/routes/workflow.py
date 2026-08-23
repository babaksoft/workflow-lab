from typing import Annotated

from fastapi import APIRouter, Depends

from workflow_lab.api.dependencies import get_workflow
from workflow_lab.api.instrument import (
    WORKFLOW_ERRORS,
    WORKFLOW_EXECUTIONS,
    WORKFLOW_LATENCY,
)
from workflow_lab.api.schemas import WorkflowResponse
from workflow_lab.utils import Timer
from workflow_lab.workflows import GeneratorJudgeFlow

router = APIRouter(prefix="/workflow", tags=["workflow"])


@router.post("", response_model=WorkflowResponse)
async def run_workflow(
    workflow: Annotated[GeneratorJudgeFlow, Depends(get_workflow)],
) -> WorkflowResponse:
    """
    Executes the Generator-Judge workflow.

    Returns:
        Workflow response containing the judge LLM verdict.

    Raises:
        Exception:
            If workflow execution fails.
    """

    workflow_name = workflow.workflow_name
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
