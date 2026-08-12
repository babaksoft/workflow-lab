from fastapi import FastAPI

from workflow_lab.api.routes.workflow import router as workflow_router

app = FastAPI(
    title="Workflow Lab",
    version="0.1.0",
)

app.include_router(workflow_router, prefix="/api/v1")
