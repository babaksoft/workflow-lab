import asyncio

from workflow_lab.config.logging import configure_logging
from workflow_lab.config.settings import load_environment
from workflow_lab.experiments.llm_observability.generator_judge_flow import (
    GeneratorJudgeFlow,
)
from workflow_lab.experiments.llm_observability.providers.provider_factory import (
    create_provider,
)
from workflow_lab.utils.instrumentation import instrument


async def main() -> None:
    load_environment()
    configure_logging()
    instrument()

    provider = create_provider(
        provider="bedrock",
        model="mistral.mistral-7b-instruct-v0:2",
    )

    workflow = GeneratorJudgeFlow(
        provider=provider,
        timeout=60,
    )

    result = await workflow.run()

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
