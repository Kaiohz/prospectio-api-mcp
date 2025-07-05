import contextlib
from fastapi import FastAPI
from application.api.routes import mcp
from application.api.routes import api_router
from config import MantiksConfig
from domain.ports.prospect_api import ProspectAPIPort
from infrastructure.services.mantiks import MantiksAPI
from infrastructure.services.clearbit import ClearbitAPI
from infrastructure.services.hunter import HunterAPI
from infrastructure.services.peopledatalabs import PeopleDataLabsAPI
from infrastructure.services.apollo import ApolloAPI
from infrastructure.services.cognism import CognismAPI
from infrastructure.services.leadgenius import LeadGeniusAPI
from infrastructure.services.dropcontact import DropcontactAPI
from infrastructure.services.lusha import LushaAPI
from infrastructure.services.zoominfo import ZoomInfoAPI
from infrastructure.services.scrubby import ScrubbyAPI
from domain.services.leads.mantiks import MantiksStrategy
from domain.services.leads.clearbit import ClearbitStrategy
from domain.services.leads.hunter import HunterStrategy
from domain.services.leads.peopledatalabs import PeopleDataLabsStrategy
from domain.services.leads.apollo import ApolloStrategy
from domain.services.leads.cognism import CognismStrategy
from domain.services.leads.leadgenius import LeadGeniusStrategy
from domain.services.leads.dropcontact import DropcontactStrategy
from domain.services.leads.lusha import LushaStrategy
from domain.services.leads.zoominfo import ZoomInfoStrategy
from domain.services.leads.scrubby import ScrubbyStrategy

PROSPECT_STRATEGIES: dict[str, ProspectAPIPort] = {
    "mantiks": MantiksStrategy(port=MantiksAPI(MantiksConfig())),
    "clearbit": ClearbitStrategy(port=ClearbitAPI()),
    "hunter": HunterStrategy(port=HunterAPI()),
    "peopledatalabs": PeopleDataLabsStrategy(port=PeopleDataLabsAPI()),
    "apollo": ApolloStrategy(port=ApolloAPI()),
    "cognism": CognismStrategy(port=CognismAPI()),
    "leadgenius": LeadGeniusStrategy(port=LeadGeniusAPI()),
    "dropcontact": DropcontactStrategy(port=DropcontactAPI()),
    "lusha": LushaStrategy(port=LushaAPI()),
    "zoominfo": ZoomInfoStrategy(port=ZoomInfoAPI()),
    "scrubby": ScrubbyStrategy(port=ScrubbyAPI()),
}

# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp.session_manager.run())
        yield

app = FastAPI(title="Prospectio API", lifespan=lifespan)
REST_PATH = "/rest/v1"
MCP_PATH = "/prospectio/"

app.include_router(api_router, prefix=REST_PATH, tags=["Prospects"])
app.mount(MCP_PATH, mcp.streamable_http_app())





