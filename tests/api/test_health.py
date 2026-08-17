import pytest
from fastapi.testclient import TestClient

from workflow_lab.api.main import create_app
from workflow_lab.config import settings


@pytest.fixture
def client() -> TestClient:
    """
    Provides a test client that disables Phoenix instrumentation.

    Returns:
        Configured FastAPI test client.
    """

    return TestClient(create_app(phoenix_enabled=False))


def test_health_check_returns_healthy_status(
    client: TestClient,
) -> None:
    """Verify the health endpoint returns a healthy status.

    Args:
        client:
            FastAPI test client.
    """

    response = client.get(f"{settings.API_URL_PREFIX}/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }
