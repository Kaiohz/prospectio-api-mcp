import contextlib
from typing import Callable
from fastapi import FastAPI
from application.api.leads_routes import leads_router
from application.api.profile_routes import profile_router
from infrastructure.services.profile_database import ProfileDatabase
from mcp_routes import mcp_prospectio
from config import ActiveJobsDBConfig, JsearchConfig, MantiksConfig
from domain.services.leads.active_jobs_db import ActiveJobsDBStrategy
from domain.services.leads.jsearch import JsearchStrategy
from domain.services.leads.mantiks import MantiksStrategy
from infrastructure.services.active_jobs_db import ActiveJobsDBAPI
from infrastructure.services.jsearch import JsearchAPI
from infrastructure.services.mantiks import MantiksAPI
from mcp_routes import mcp_router
from config import Config
from infrastructure.services.leads_database import LeadsDatabase
from config import DatabaseConfig

_LEADS_STRATEGIES: dict[str, Callable] = {
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
}

jobs_routes = leads_router(
    _LEADS_STRATEGIES, LeadsDatabase(DatabaseConfig().DATABASE_URL)
)

profile_routes = profile_router(ProfileDatabase(DatabaseConfig().DATABASE_URL))


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the lifespan of both HTTP and stdio MCP servers."""
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp_prospectio.session_manager.run())
        yield


app = FastAPI(title="Prospectio API", lifespan=lifespan)
REST_PATH = "/prospectio/rest/v1"
MCP_PATH = "/prospectio/"

app.include_router(jobs_routes, prefix=REST_PATH, tags=["Prospects"])
app.include_router(mcp_router, prefix=REST_PATH, tags=["MCP Prospectio"])
app.include_router(profile_routes, prefix=REST_PATH, tags=["Profile"])

app.mount(MCP_PATH, mcp_prospectio.streamable_http_app())

if __name__ == "__main__":
    if Config().EXPOSE == "stdio":
        mcp_prospectio.run(transport="stdio")
