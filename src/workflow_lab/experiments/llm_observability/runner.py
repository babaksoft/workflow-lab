import asyncio

from workflow_lab.config.logging import configure_logging
from workflow_lab.providers import create_provider
from workflow_lab.utils.instrumentation import instrument
from workflow_lab.workflows.generator_judge_flow import (
    GeneratorJudgeFlow,
)


async def main() -> None:
    configure_logging()
    instrument()  # MUST run `phoenix serve` before `main` executes

    provider = create_provider(
        provider="bedrock",
        model="mistral.mistral-7b-instruct-v0:2",
    )

    workflow = GeneratorJudgeFlow(
        provider=provider,
        workflow_name="Test Workflow",
        timeout=60,
    )

    result = await workflow.run()

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
