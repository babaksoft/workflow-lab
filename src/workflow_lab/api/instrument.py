from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from prometheus_client import Counter, Histogram

from workflow_lab.utils import Timer

HTTP_REQUESTS = Counter(
    "workflow_lab_http_requests_total",
    "Total number of HTTP requests.",
    labelnames=("method", "route", "status"),
)

HTTP_REQUEST_LATENCY = Histogram(
    "workflow_lab_http_request_duration_seconds",
    "HTTP request latency in seconds.",
    labelnames=("method", "route"),
)

HTTP_ERRORS = Counter(
    "workflow_lab_http_errors_total",
    "Total number of HTTP request errors.",
    labelnames=("method", "route"),
)

WORKFLOW_EXECUTIONS = Counter(
    "workflow_lab_workflow_executions_total",
    "Total number of workflow executions.",
    labelnames=("workflow",),
)

WORKFLOW_LATENCY = Histogram(
    "workflow_lab_workflow_duration_seconds",
    "Workflow execution latency in seconds.",
    labelnames=("workflow",),
)

WORKFLOW_ERRORS = Counter(
    "workflow_lab_workflow_errors_total",
    "Total number of workflow execution errors.",
    labelnames=("workflow",),
)


async def instrument_http_request(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """
    Collects HTTP request metrics.

    Args:
        request:
            Incoming HTTP request.

        call_next:
            Callable that invokes the next middleware or route handler.

    Returns:
        HTTP response produced by the application.

    Raises:
        Exception:
            If request processing fails.
    """

    method = request.method
    route = request.url.path

    with Timer() as timer:
        try:
            response = await call_next(request)
        except Exception:
            HTTP_ERRORS.labels(
                method=method,
                route=route,
            ).inc()
            raise

    status = str(response.status_code)

    HTTP_REQUESTS.labels(
        method=method,
        route=route,
        status=status,
    ).inc()

    HTTP_REQUEST_LATENCY.labels(
        method=method,
        route=route,
    ).observe(timer.elapsed)

    return response
