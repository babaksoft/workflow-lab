# mypy: disable-error-code="import-untyped"
from llama_index.llms.ollama import Ollama

from workflow_lab.config.settings import OLLAMA_BASE_URL
from workflow_lab.providers.llm_provider import LLMProvider


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
            Generated response from the LLM.
        """

        llm = Ollama(model=self._model, base_url=OLLAMA_BASE_URL)
        response = await llm.acomplete(prompt)

        return str(response.text)
