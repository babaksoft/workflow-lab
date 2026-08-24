import json

from pydantic import BaseModel, Field
from workflows import Workflow, step
from workflows.events import Event, StartEvent, StopEvent

from workflow_lab.prompts.generator_judge import (
    GENERATOR_PROMPT,
    JUDGE_PROMPT,
)
from workflow_lab.providers import LLMProvider


class JudgeResult(BaseModel):
    """
    Represents the judge's evaluation of the generated answer.

    Attributes:
        constraint_handling:
            Grading result for constraint handling.

        word_counting:
            Grading result for word counting.

        word_filtering:
            Grading result for word filtering.

        justification:
            Justification of grading results for each rubric.
    """

    constraint_handling: int = Field(
        ..., description="Grading result for constraint handling.", ge=1, le=10
    )

    word_counting: int = Field(
        ..., description="Grading result for word counting.", ge=1, le=10
    )

    word_filtering: int = Field(
        ..., description="Grading result for word filtering.", ge=1, le=10
    )

    justification: dict[str, str] = Field(
        ...,
        description="Justification of grading results for each rubric.",
    )


class ResponseEvent(Event):
    response: str


class GeneratorJudgeFlow(Workflow):
    """Generates an answer and evaluates it with a second LLM call."""

    def __init__(
        self,
        provider: LLMProvider,
        *,
        workflow_name: str,
        timeout: float = 60,
        verbose: bool = False,
    ) -> None:
        """
        Initialize the workflow instance.

        Args:
            provider:
                Language model provider.

            workflow_name:
                Workflow name used for instrumentation.

            timeout:
                Maximum seconds to wait for workflow completion.
                Default is 60 seconds.

            verbose:
                Whether to print step activity during execution.
                Default is False.
        """

        super().__init__(timeout=timeout, verbose=verbose)
        self._workflow_name = workflow_name
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

        return ResponseEvent(
            response=await self._provider.generate(GENERATOR_PROMPT),
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

        prompt = JUDGE_PROMPT.format(response=ev.response)
        response = await self._provider.generate(prompt)

        try:
            result = JudgeResult.model_validate(json.loads(response))
        except (json.JSONDecodeError, ValueError) as exc:
            raise ValueError("Judge returned invalid JSON.") from exc

        return StopEvent(result=result.model_dump())
