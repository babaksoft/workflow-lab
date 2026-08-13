from llama_index.llms.openai import OpenAI

from workflow_lab.experiments.llm_observability.llm_provider import LLMProvider


class OpenAIProvider(LLMProvider):
    """Provides LLM generation through OpenAI."""

    def __init__(self, model: str) -> None:
        self._model = model

    async def generate(self, prompt: str) -> str:
        """
        Generates a response using an OpenAI model.

        Args:
            prompt:
                Prompt sent to the LLM.

        Returns:
            Generated text.
        """

        llm = OpenAI(model=self._model)

        response = await llm.acomplete(prompt)

        return response.text
