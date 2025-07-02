from fastapi import APIRouter, HTTPException
from mcp.server.fastmcp import FastMCP
from application.ports.prospect_api import ProspectAPIPort
from application.use_cases.get_leads import GetLeadsUseCase
from config import MantiksConfig
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
import logging
import traceback

mcp = FastMCP(name="Prospectio MCP", stateless_http=True)  
api_router = APIRouter()

logger = logging.getLogger(__name__)

prospect_source_mapping: dict[str, ProspectAPIPort] = {
    "mantiks": MantiksAPI(MantiksConfig()),
    "clearbit": ClearbitAPI(),
    "hunter": HunterAPI(),
    "peopledatalabs": PeopleDataLabsAPI(),
    "apollo": ApolloAPI(),
    "cognism": CognismAPI(),
    "leadgenius": LeadGeniusAPI(),
    "dropcontact": DropcontactAPI(),
    "lusha": LushaAPI(),
    "zoominfo": ZoomInfoAPI(),
    "scrubby": ScrubbyAPI(),
}

@api_router.get("/leads/{source}")
@mcp.tool(description="Get leads with contacts from the specified source. " \
"the first parameter is the source, the second parameter is the location country code.")
async def get_leads(source: str, location: str) -> dict:
    """
    Get leads with contacts from the specified source.
    
    :param source: The source from which to get leads with contacts.
    :return: A string indicating the success of the operation.
    """
    try:
        port = prospect_source_mapping.get(source)
        return await GetLeadsUseCase(source, location, port).get_leads()
    except Exception as e:
        logger.error(f"Error in get_leads: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

