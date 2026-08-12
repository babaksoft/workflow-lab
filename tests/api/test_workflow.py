from fastapi.testclient import TestClient

from workflow_lab.api.main import app

client = TestClient(app)


def test_run_workflow() -> None:
    """
    Verifies that the workflow endpoint executes successfully.
    """

    response = client.post("/api/v1/workflow")

    assert response.status_code == 200
    assert response.json() == {"result": 4}
