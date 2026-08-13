from workflow_lab.experiments.llm_observability.bedrock_provider import (
    BedrockProvider,
)
from workflow_lab.experiments.llm_observability.llm_provider import (
    LLMProvider,
)
from workflow_lab.experiments.llm_observability.ollama_provider import (
    OllamaProvider,
)
from workflow_lab.experiments.llm_observability.openai_provider import (
    OpenAIProvider,
)


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

    providers = {
        "openai": OpenAIProvider,
        "bedrock": BedrockProvider,
        "ollama": OllamaProvider,
    }

    try:
        provider_class = providers[provider.lower()]
    except KeyError as exc:
        raise ValueError(f"Unsupported LLM provider: {provider}") from exc

    return provider_class(model=model)
