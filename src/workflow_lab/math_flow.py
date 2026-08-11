import asyncio

from workflows import Workflow, step
from workflows.events import StartEvent, StopEvent


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

        return StopEvent(result=2 + 2)


async def main() -> None:
    workflow = MathFlow(workflow_name="Simple Math", timeout=30, verbose=False)
    print(f"Workflow started: workflow_name='{workflow.workflow_name}'")

    result = await workflow.run()

    print(f"Workflow '{workflow.workflow_name}' completed: result={result!s}")


if __name__ == "__main__":
    asyncio.run(main())
