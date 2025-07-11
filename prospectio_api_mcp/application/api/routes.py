from fastapi import APIRouter, HTTPException, Query, Path
from mcp.server.fastmcp import FastMCP
from application.use_cases.get_leads import GetCompanyJobsUseCase
from collections.abc import Callable
import logging
import traceback
from domain.services.leads.strategy import CompanyJobsStrategy
from prospectio_api_mcp.domain.entities.leads import Leads


mcp_company_jobs = FastMCP(name="Prospectio MCP", stateless_http=True)
logger = logging.getLogger(__name__)


def get_company_jobs_router(jobs_strategy: dict[str, Callable[[str, list[str]], CompanyJobsStrategy]]) -> APIRouter:
    """
    Create an APIRouter for company jobs endpoints with injected strategy.

    Args:
        jobs_strategy (dict[str, callable]): Mapping of source to strategy factory.

    Returns:
        APIRouter: Configured router with endpoints.
    """
    company_jobs_router = APIRouter()

    @company_jobs_router.get("/company/jobs/{source}")
    @mcp_company_jobs.tool(
        description="Get companies jobs with contacts from the specified source."
        "the first parameter is the source, it can be mantiks, jsearch, active_jobs_db or mock."
        "The second parameter is the location country code, and the third parameter is a list of job titles.",
    )
    async def get_company_jobs(
        source: str = Path(..., description="Lead source"),
        location: str = Query(..., description="Location country code"),
        job_title: list[str] = Query(
            ..., description="Job titles (repeat this param for multiple values)"
        ),
    ) -> Leads:
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
            if source not in jobs_strategy:
                raise ValueError(f"Unknown source: {source}")
            strategy = jobs_strategy[source](location, job_title)
            return await GetCompanyJobsUseCase(strategy).get_leads()
        except Exception as e:
            logger.error(f"Error in get company jobs: {e}\n{traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

    return company_jobs_router
