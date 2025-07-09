import contextlib
from typing import Callable
from fastapi import FastAPI
from application.api.routes import get_company_jobs_router, mcp_company_jobs
from config import ActiveJobsDBConfig, JsearchConfig, MantiksConfig, MockConfig
from domain.services.leads.active_jobs_db import ActiveJobsDBStrategy
from domain.services.leads.jsearch import JsearchStrategy
from domain.services.leads.mantiks import MantiksStrategy
from domain.services.leads.mock import MockStrategy
from infrastructure.services.active_jobs_db import ActiveJobsDBAPI
from infrastructure.services.jsearch import JsearchAPI
from infrastructure.services.mantiks import MantiksAPI
from infrastructure.services.mock import MockAPI
from mcp_routes import mcp_router
from config import Config

_COMPANY_JOBS_STRATEGIES: dict[str, Callable] = {
    "mantiks": lambda location, job_title: MantiksStrategy(
        port=MantiksAPI(MantiksConfig()), location=location, job_title=job_title
    ),
    "jsearch": lambda location, job_title: JsearchStrategy(
        port=JsearchAPI(JsearchConfig()), location=location, job_title=job_title
    ),
    "active_jobs_db": lambda location, job_title: ActiveJobsDBStrategy(
        port=ActiveJobsDBAPI(ActiveJobsDBConfig()),
        location=location,
        job_title=job_title,
    ),
    "mock": lambda location, job_title: MockStrategy(
        port=MockAPI(MockConfig()), location=location, job_title=job_title
    ),
}

# Create Company Jobs Routes object
jobs_routes = get_company_jobs_router(_COMPANY_JOBS_STRATEGIES)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the lifespan of both HTTP and stdio MCP servers."""
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp_company_jobs.session_manager.run())
        yield


app = FastAPI(title="Prospectio API", lifespan=lifespan)
REST_PATH = "/rest/v1"
MCP_PATH = "/prospectio/"
app.include_router(jobs_routes, prefix=REST_PATH, tags=["Prospects"])
app.include_router(mcp_router, prefix=REST_PATH, tags=["MCP Company Jobs"])
app.mount(MCP_PATH, mcp_company_jobs.streamable_http_app())

if __name__ == "__main__":
    if Config().EXPOSE == "stdio":
        mcp_company_jobs.run(transport="stdio")
