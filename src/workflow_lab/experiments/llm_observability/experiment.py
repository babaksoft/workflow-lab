import asyncio
import logging

from workflow_lab.config.logging import configure_logging
from workflow_lab.experiments.llm_observability.provider_factory import (
    BedrockProvider,
    LLMProvider,
    OllamaProvider,
    OpenAIProvider,
    create_provider,
)

logger = logging.getLogger(__name__)


def show_banner() -> str:
    print("\n============================================")
    print("LLM Observability Demo\n")
    print("Main objective:")
    print("   Evaluating Phoenix observability using")
    print("   different LlamaIndex LLM integrations.")
    print("============================================\n")

    return input("Press <ENTER> to continue... (or q to quit)\n")


async def main() -> None:
    choice = show_banner()
    if choice.lower() == "q":
        return

    print("Some cool stuff coming soon!")


if __name__ == "__main__":
    asyncio.run(main())
