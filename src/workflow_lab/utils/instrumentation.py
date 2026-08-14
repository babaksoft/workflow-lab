from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from phoenix.otel import register

from workflow_lab.config import settings


def instrument() -> None:
    """
    Start generating traces using LlamaIndex OpenInference integration.
    """

    tracer_provider = register(
        endpoint=settings.PHOENIX_COLLECTOR_ENDPOINT,
        project_name=settings.PHOENIX_PROJECT_NAME,
        protocol="http/protobuf",
    )
    LlamaIndexInstrumentor().instrument(
        tracer_provider=tracer_provider,
    )
