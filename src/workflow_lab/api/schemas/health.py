from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """
    Response model for API health checks.

    Attributes:
        status:
            Current health status of the API.
    """

    status: str = Field(
        ...,
        description="Current health status of the API.",
        examples=["healthy"],
    )
