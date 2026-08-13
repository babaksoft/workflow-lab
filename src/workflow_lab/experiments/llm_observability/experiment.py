import asyncio
import logging

from workflow_lab.config.logging import configure_logging
from workflow_lab.config.settings import load_environment
from workflow_lab.experiments.llm_observability.providers.provider_factory import (
    create_provider,
)

logger = logging.getLogger(__name__)


def show_banner() -> str:
    print("\n==================================================")
    print("LLM Observability Demo\n")
    print("Main objective:")
    print("   Evaluating LlamaIndex LLM integrations using")
    print("   a local Arize Phoenix server.")
    print("==================================================\n")

    return input("Press <ENTER> to continue... (or q to quit)\n")


async def main() -> None:
    load_environment()
    configure_logging()

    choice = show_banner()
    if choice.lower() == "q":
        return

    prompt = "Reply with exactly: Hello"

    # Test Bedrock provider
    model = "mistral.mistral-7b-instruct-v0:2"
    logger.info(
        "Calling Bedrock model: model='%s' prompt='%s'",
        model,
        prompt,
    )

    llm = create_provider(provider="bedrock", model=model)
    response = await llm.generate(prompt)

    logger.info("Bedrock model response: '%s'", response)

    # Test Ollama provider
    model = "gpt-oss:20b-cloud"
    logger.info(
        "Calling Ollama model: model='%s' prompt='%s'",
        model,
        prompt,
    )

    llm = create_provider(provider="ollama", model=model)
    response = await llm.generate(prompt)

    logger.info("Ollama model response: '%s'", response)

    # Test OpenAI provider
    model = "gpt-4o-mini"
    logger.info(
        "Calling OpenAI model: model='%s' prompt='%s'",
        model,
        prompt,
    )

    llm = create_provider(provider="openai", model=model)
    response = await llm.generate(prompt)

    logger.info("OpenAI model response: '%s'", response)


if __name__ == "__main__":
    asyncio.run(main())
