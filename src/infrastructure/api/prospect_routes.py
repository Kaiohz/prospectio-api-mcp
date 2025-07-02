from fastapi import APIRouter, HTTPException
from mcp.server.fastmcp import FastMCP
from application.ports.get_leads import ProspectAPIPort
from application.use_cases.get_leads import GetLeadsContactsUseCase
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

mcp = FastMCP(name="Prospectio MCP", stateless_http=True)  
api_router = APIRouter()

prospect_source_mapping: dict[str, ProspectAPIPort] = {
    "mantiks": MantiksAPI(),
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
@mcp.tool(description="Get leads with contacts from the specified source.")
async def get_leads(source: str) -> dict:
    """
    Get leads with contacts from the specified source.
    
    :param source: The source from which to get leads with contacts.
    :return: A string indicating the success of the operation.
    """
    try:
        port = prospect_source_mapping.get(source)
        return await GetLeadsContactsUseCase(source, port).get_leads()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    