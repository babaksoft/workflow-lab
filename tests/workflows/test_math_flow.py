from workflow_lab.workflows import MathFlow


async def test_math_flow_returns_expected_result() -> None:
    """
    Verifies that the math workflow completes with the expected result.
    """

    workflow = MathFlow(workflow_name="Test Math", timeout=30)

    result = await workflow.run()

    assert result == {"value": 4}
