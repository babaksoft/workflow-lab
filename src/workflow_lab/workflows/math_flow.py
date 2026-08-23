import asyncio
import logging

from workflows import Workflow, step
from workflows.events import StartEvent, StopEvent

from workflow_lab.config.logging import configure_logging
from workflow_lab.utils import instrument

logger = logging.getLogger(__name__)


class MathFlow(Workflow):
    @step
    async def calculate(self, ev: StartEvent) -> StopEvent:
        """
        Performs a simple math calculation.

        Args:
            ev:
                Start event triggering workflow start.

        Returns:
            Stop event triggering workflow completion.
        """

        return StopEvent(result={"value": 2 + 2})


async def main() -> None:
    configure_logging()
    instrument()

    workflow = MathFlow(workflow_name="Simple Math", timeout=30, verbose=False)
    logger.info(
        "Workflow started: workflow_name='%s'",
        workflow.workflow_name,
    )

    result = await workflow.run()

    logger.info(
        "Workflow '%s' completed: result=%d",
        workflow.workflow_name,
        result,
    )


if __name__ == "__main__":
    asyncio.run(main())
