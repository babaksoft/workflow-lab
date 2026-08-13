import json

from pydantic import BaseModel, Field
from workflows import Workflow, step
from workflows.events import Event, StartEvent, StopEvent

from workflow_lab.providers import LLMProvider


class JudgeResult(BaseModel):
    """Represents the judge's evaluation of the generated answer."""

    constraint_handling: int = Field(ge=1, le=10)
    word_counting: int = Field(ge=1, le=10)
    word_filtering: int = Field(ge=1, le=10)
    justification: dict[str, str]


class ResponseEvent(Event):
    response: str


class GeneratorJudgeFlow(Workflow):
    """Generates an answer and evaluates it with a second LLM call."""

    def __init__(
        self,
        provider: LLMProvider,
        *,
        timeout: float = 60,
        verbose: bool = False,
    ) -> None:
        super().__init__(timeout=timeout, verbose=verbose)
        self._provider = provider

    @step
    async def generate(self, ev: StartEvent) -> ResponseEvent:
        """
        Generates four constrained bullet points about Python generators.

        Args:
            ev:
                Start event triggering answer generation.

        Returns:
            Response event containing the generated answer.
        """

        prompt = """Write exactly 4 bullet points about Python generators.

Constraints:

* Each bullet must contain exactly 10 words.
* Do not use the words "lazy", "memory", or "iterator".
"""
        return ResponseEvent(
            response=await self._provider.generate(prompt),
        )

    @step
    async def judge(self, ev: ResponseEvent) -> StopEvent:
        """
        Evaluates the generated answer against the required constraints.

        Args:
            ev:
                Response event containing generated answer from
                the previous workflow step.

        Returns:
            Stop event containing the judge result.

        Raises:
            ValueError:
                If the judge does not return valid JSON.
        """

        prompt = f"""Evaluate the following answer according to these requirements.

Generation requirements:

* The answer must contain exactly 4 bullet points.
* Each bullet must contain exactly 10 words.
* The words "lazy", "memory", and "iterator" must not appear.

Evaluate these rubrics:

* constraint_handling: Does the answer follow all generation requirements?
* word_counting: Does each bullet contain exactly 10 words?
* word_filtering: Does the answer avoid all forbidden words?

Return ONLY valid JSON with exactly this structure:

{{
    "constraint_handling": <integer from 1 to 10>,
    "word_counting": <integer from 1 to 10>,
    "word_filtering": <integer from 1 to 10>,
    "justification": {{
        "constraint_handling": "<short justification>",
        "word_counting": "<short justification>",
        "word_filtering": "<short justification>"
    }}
}}

Answer to judge:

{ev.response}
"""

        response = await self._provider.generate(prompt)

        try:
            result = JudgeResult.model_validate(json.loads(response))
        except (json.JSONDecodeError, ValueError) as exc:
            raise ValueError("Judge returned invalid JSON.") from exc

        return StopEvent(result=result.model_dump())
