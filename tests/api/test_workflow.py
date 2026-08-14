from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from workflow_lab.api.dependencies import get_workflow
from workflow_lab.api.main import create_app
from workflow_lab.workflows.math_flow import MathFlow


def get_test_workflow() -> MathFlow:
    """
    Retrieve a test instance of the deterministic MathFlow.

    Returns:
        Test MathFlow instance.
    """

    return MathFlow(workflow_name="Test Math", timeout=30)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """
    Provides a test client using the deterministic MathFlow.

    Returns:
        Configured FastAPI test client.
    """

    app = create_app(phoenix_enabled=False)
    app.dependency_overrides[get_workflow] = get_test_workflow

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_run_workflow(client: TestClient) -> None:
    """
    Verifies that the workflow endpoint executes successfully.
    """

    response = client.post("/api/v1/workflow")

    assert response.status_code == 200
    assert response.json() == {"result": {"value": 4}}
