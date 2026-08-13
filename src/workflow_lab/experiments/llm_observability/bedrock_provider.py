from llama_index.llms.bedrock import Bedrock

from workflow_lab.experiments.llm_observability.llm_provider import LLMProvider


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
            Generated text.
        """

        llm = Bedrock(model=self._model)

        response = await llm.acomplete(prompt)

        return response.text
