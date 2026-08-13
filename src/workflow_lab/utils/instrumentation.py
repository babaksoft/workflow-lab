from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from phoenix.otel import register


def instrument() -> None:
    """
    Start generating traces using LlamaIndex OpenInference integration.
    """

    tracer_provider = register(
        project_name="workflow-lab-otel",
        protocol="http/protobuf",
    )
    LlamaIndexInstrumentor().instrument(
        tracer_provider=tracer_provider,
    )
