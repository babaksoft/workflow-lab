# mypy: disable-error-code="import-untyped"
from llama_index.llms.ollama import Ollama

from workflow_lab.experiments.llm_observability.providers.llm_provider import (
    LLMProvider,
)


class OllamaProvider(LLMProvider):
    """Provides LLM generation through Ollama."""

    def __init__(self, model: str) -> None:
        self._model = model

    async def generate(self, prompt: str) -> str:
        """
        Generates a response using an Ollama model.

        Args:
            prompt:
                Prompt sent to the LLM.

        Returns:
            Generated text.
        """

        llm = Ollama(model=self._model)

        response = await llm.acomplete(prompt)

        return str(response.text)
