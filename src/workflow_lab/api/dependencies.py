import os

from workflow_lab.providers import create_provider
from workflow_lab.workflows import GeneratorJudgeFlow

LLM_PROVIDER = "openai"
LLM_MODEL = "gpt-4o-mini"


def get_workflow() -> GeneratorJudgeFlow:
    """
    Provides the workflow used by the API.

    Returns:
        Configured workflow instance.
    """

    provider = create_provider(
        provider=os.getenv("LLM_PROVIDER", LLM_PROVIDER),
        model=os.getenv("LLM_MODEL", LLM_MODEL),
    )

    workflow_name = "Generator Judge"
    return GeneratorJudgeFlow(
        provider=provider,
        workflow_name=workflow_name,
        timeout=30,
        verbose=False,
    )
