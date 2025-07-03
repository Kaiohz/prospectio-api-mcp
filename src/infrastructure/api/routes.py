from fastapi import APIRouter, HTTPException, Query, Path
from mcp.server.fastmcp import FastMCP
from domain.ports.prospect_api import ProspectAPIPort
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
async def get_leads(
    source: str = Path(..., description="Lead source"),
    location: str = Query(..., description="Location country code"),
    job_title: list[str] = Query(..., description="Job titles (repeat this param for multiple values)")
) -> dict:
    """
    Retrieve leads with contacts from the specified source.

    Args:
        source (str): The source from which to get leads with contacts.
        location (str): The country code for the location.
        job_title (list[str]): List of job titles to filter leads.

    Returns:
        dict: A dictionary containing the leads data.
    """
    try:
        port = prospect_source_mapping.get(source)
        return await GetLeadsUseCase(source, location, job_title, port).get_leads()
    except Exception as e:
        logger.error(f"Error in get_leads: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

