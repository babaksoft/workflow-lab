from fastapi import FastAPI

from workflow_lab.api.instrument import instrument_http_request
from workflow_lab.api.routes.metrics import router as metrics_router
from workflow_lab.api.routes.workflow import router as workflow_router

app = FastAPI(
    title="Workflow Lab",
    version="0.1.0",
)

app.middleware("http")(instrument_http_request)

app.include_router(workflow_router, prefix="/api/v1")
app.include_router(metrics_router, prefix="/api/v1")
