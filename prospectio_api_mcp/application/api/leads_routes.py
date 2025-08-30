from typing import Union
from fastapi import APIRouter, Body, HTTPException, Path
from application.use_cases.get_leads import GetLeadsUseCase
from domain.entities.company import CompanyEntity
from domain.entities.contact import ContactEntity
from domain.entities.job import JobEntity
from domain.entities.leads import Leads
from domain.entities.leads_result import LeadsResult
from domain.ports.compatibility_score import CompatibilityScorePort
from domain.ports.enrich_leads import EnrichLeadsPort
from domain.ports.profile_respository import ProfileRepositoryPort
from domain.services.leads.leads_processor import LeadsProcessor
from prospectio_api_mcp.application.use_cases.insert_leads import (
    InsertLeadsUseCase,
)
from collections.abc import Callable
import logging
import traceback
from domain.services.leads.strategy import LeadsStrategy
from domain.ports.leads_repository import LeadsRepositoryPort
from application.api.mcp_routes import mcp_prospectio


logger = logging.getLogger(__name__)


def leads_router(
    jobs_strategy: dict[str, Callable[[str, list[str]], LeadsStrategy]],
    repository: LeadsRepositoryPort,
    compatibility: CompatibilityScorePort,
    profile_repository: ProfileRepositoryPort,
    enrich_port: EnrichLeadsPort,
) -> APIRouter:
    """
    Create an APIRouter for company jobs endpoints with injected strategy.

    Args:
        jobs_strategy (dict[str, callable]): Mapping of source to strategy factory.
        repository (LeadsRepositoryPort): Repository for data persistence.
    Returns:
        APIRouter: Configured router with endpoints.
    """
    company_jobs_router = APIRouter()

    @company_jobs_router.get("/leads/{type}/{offset}")
    @mcp_prospectio.tool(
        description="ALWAYS USE THIS FIRST to retrieve existing data from the database before searching for new opportunities. "
        "Returns companies, jobs, contacts or leads that are already stored in the database. "
        "This endpoint is paginated: use the 'offset' parameter to paginate through results. Offset begins at 0. "
        "Pagination size: 5 for companies, 10 for contacts, 3 for jobs. "
        "Use this tool when the user wants to see existing leads, companies, jobs, or contacts. "
        "Only use the insert/leads endpoint when the user specifically asks for new opportunities or when no relevant data is found in the database. "
        "The parameter 'type' can be: 'companies', 'jobs', 'contacts', or 'leads'. "
        "Example: GET /get/leads/companies/0 to get the first 5 companies, /get/leads/companies/5 for the next 5, /get/leads/contacts/0 for the first 10 contacts, /get/leads/jobs/0 for the first 3 jobs, etc."
    )
    async def get_leads(
        type: str = Path(..., description="Lead source"),
        offset: int = Path(..., description="Offset for pagination"),
    ) -> Union[Leads, CompanyEntity, JobEntity, ContactEntity]:
        try:
            leads = await GetLeadsUseCase(type, repository).get_leads(offset)
            return leads
        except Exception as e:
            logger.error(f"Error in get leads: {e}\n{traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

    @company_jobs_router.post("/insert/leads")
    @mcp_prospectio.tool(
        description="Use this ONLY when the user asks for NEW opportunities or when get/leads returns insufficient data. "
        "This tool searches external sources and inserts NEW leads into the database. "
        "Sources available: 'mantiks', 'jsearch', 'active_jobs_db'."
        "If a source does not work or returns no data, try another one. "
        "Requires location (country code) and job titles as technologies (e.g., 'Python', 'AI', 'RAG', 'LLM'). "
        "IMPORTANT: Before using this, check the user profile or ask to update it if missing. "
        'Example JSON: {"source": "mantiks", "location": "FR", "job_title": ["Python", "AI", "RAG", "LLM"]}'
    )
    async def insert_leads(
        source: str = Body(..., description="Lead source"),
        location: str = Body(..., description="Location country code"),
        job_title: list[str] = Body(
            ..., description="Job titles (repeat this param for multiple values)"
        ),
    ) -> LeadsResult:
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
            job_title = [title.strip().lower() for title in job_title]
            location = location.strip().lower()
            strategy = jobs_strategy[source](location, job_title)
            processor = LeadsProcessor(compatibility)
            leads = await InsertLeadsUseCase(
                strategy, repository, processor, profile_repository, enrich_port
            ).insert_leads()
            return leads
        except Exception as e:
            logger.error(f"Error in insert leads: {e}\n{traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

    return company_jobs_router
