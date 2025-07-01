from fastapi import APIRouter, HTTPException
from mcp.server.fastmcp import FastMCP
from application.ports.leads.get_leads import ProspectAPIPort
from application.use_cases.leads.get_leads import GetLeadsContactsUseCase
from infrastructure.services.mantiks import MantiksAPI

mcp = FastMCP(name="Prospectio MCP", stateless_http=True)  
api_router = APIRouter()

prospect_source_mapping: dict[str, ProspectAPIPort] = {
    "mantiks": MantiksAPI(),
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

    