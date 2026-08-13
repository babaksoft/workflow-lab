from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Defines the common interface for experimental LLM providers."""

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """
        Generates a response for the supplied prompt.

        Args:
            prompt:
                Prompt sent to the LLM.

        Raises:
            NotImplementedError:
                If the provider does not implement generation.
        """

        raise NotImplementedError
