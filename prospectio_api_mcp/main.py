import contextlib
from typing import Callable
from fastapi import FastAPI
from application.api.leads_routes import leads_router
from application.api.profile_routes import profile_router
from infrastructure.services.compatibility_score import CompatibilityScoreLLM
from infrastructure.services.enrich_leads_agent.agent import EnrichLeadsAgent
from infrastructure.services.enrich_leads_agent.tools.crawl_client import CrawlClient
from infrastructure.services.profile_database import ProfileDatabase
from application.api.mcp_routes import mcp_prospectio
from config import ActiveJobsDBConfig, JsearchConfig
from domain.services.leads.strategies.active_jobs_db import ActiveJobsDBStrategy
from domain.services.leads.strategies.jsearch import JsearchStrategy
from infrastructure.services.active_jobs_db import ActiveJobsDBAPI
from infrastructure.services.jsearch import JsearchAPI
from config import AppConfig
from infrastructure.services.leads_database import LeadsDatabase
from config import DatabaseConfig
from config import AppConfig
from fastapi.middleware.cors import CORSMiddleware


_LEADS_STRATEGIES: dict[str, Callable] = {
    "jsearch": lambda location, job_title: JsearchStrategy(
        port=JsearchAPI(JsearchConfig()), location=location, job_title=job_title
    ),
    "active_jobs_db": lambda location, job_title: ActiveJobsDBStrategy(
        port=ActiveJobsDBAPI(ActiveJobsDBConfig()),
        location=location,
        job_title=job_title,
    ),
}

leads_routes = leads_router(
    _LEADS_STRATEGIES,
    LeadsDatabase(DatabaseConfig().DATABASE_URL),
    CompatibilityScoreLLM(),
    ProfileDatabase(DatabaseConfig().DATABASE_URL),
    EnrichLeadsAgent(),
)

profile_routes = profile_router(ProfileDatabase(DatabaseConfig().DATABASE_URL))


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the lifespan of both HTTP and stdio MCP servers."""
    async with contextlib.AsyncExitStack() as stack:
        await CrawlClient().crawl_page("https://www.google.fr")
        if AppConfig().EXPOSE == "streamable":
            await stack.enter_async_context(mcp_prospectio.session_manager.run())
        yield


app = FastAPI(title="Prospectio API", lifespan=lifespan)

app_config = AppConfig()

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REST_PATH = "/prospectio/rest/v1"
MCP_PATH = "/prospectio/"

app.include_router(leads_routes, prefix=REST_PATH, tags=["Prospects"])
app.include_router(profile_routes, prefix=REST_PATH, tags=["Profile"])

if AppConfig().EXPOSE == "streamable":
    app.mount(MCP_PATH, mcp_prospectio.streamable_http_app())
if AppConfig().EXPOSE == "sse":
    app.mount(MCP_PATH, mcp_prospectio.sse_app())

if __name__ == "__main__":
    mcp_prospectio.run(transport="stdio")
