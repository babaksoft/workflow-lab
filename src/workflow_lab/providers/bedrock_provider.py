# mypy: disable-error-code="import-untyped"
from llama_index.llms.bedrock import Bedrock

from workflow_lab.providers.llm_provider import LLMProvider


class BedrockProvider(LLMProvider):
    """Provides LLM generation through Amazon Bedrock."""

    def __init__(self, model: str) -> None:
        self._model = model

    async def generate(self, prompt: str) -> str:
        """
        Generates a response using an Amazon Bedrock model.

        Args:
            prompt:
                Prompt sent to the LLM.

        Returns:
            Generated response from the LLM.
        """

        llm = Bedrock(model=self._model)
        response = llm.complete(prompt)

        return str(response.text)
