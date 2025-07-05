from fastapi import APIRouter, HTTPException, Query, Path
from mcp.server.fastmcp import FastMCP
from application.use_cases.get_leads import GetLeadsUseCase
from prospect_strategy_factory import ProspectStrategyFactory
import logging
import traceback

mcp = FastMCP(name="Prospectio MCP", stateless_http=True)  
api_router = APIRouter()

logger = logging.getLogger(__name__)


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
        strategy_factory = ProspectStrategyFactory(source, location, job_title)
        strategy = strategy_factory.create_strategy()
        return await GetLeadsUseCase(strategy).get_leads()
    except Exception as e:
        logger.error(f"Error in get_leads: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

