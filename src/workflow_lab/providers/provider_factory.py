from workflow_lab.providers.bedrock_provider import BedrockProvider
from workflow_lab.providers.llm_provider import LLMProvider
from workflow_lab.providers.ollama_provider import OllamaProvider
from workflow_lab.providers.openai_provider import OpenAIProvider


def create_provider(provider: str, model: str) -> LLMProvider:
    """
    Creates an LLM provider for the requested provider name.

    Args:
        provider:
            Provider identifier.

        model:
            Model identifier.

    Returns:
        Configured LLM provider.

    Raises:
        ValueError:
            If the provider is unsupported.
    """

    if provider.lower() == "openai":
        return OpenAIProvider(model)

    if provider.lower() == "bedrock":
        return BedrockProvider(model)

    if provider.lower() == "ollama":
        return OllamaProvider(model)

    raise ValueError(f"Unsupported LLM provider: {provider}")
