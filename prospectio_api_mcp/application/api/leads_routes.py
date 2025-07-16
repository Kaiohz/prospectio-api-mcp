from typing import Union
from fastapi import APIRouter, Body, HTTPException, Path
from application.use_cases.get_leads import GetLeadsUseCase
from domain.entities.company import CompanyEntity
from domain.entities.contact import ContactEntity
from domain.entities.job import JobEntity
from domain.entities.leads import Leads
from domain.entities.leads_result import LeadsResult
from prospectio_api_mcp.application.use_cases.insert_leads import (
    InsertCompanyJobsUseCase,
)
from collections.abc import Callable
import logging
import traceback
from domain.services.leads.strategy import CompanyJobsStrategy
from domain.ports.leads_repository import LeadsRepositoryPort
from mcp_routes import mcp_prospectio


logger = logging.getLogger(__name__)


def leads_router(
    jobs_strategy: dict[str, Callable[[str, list[str]], CompanyJobsStrategy]],
    repository: LeadsRepositoryPort,
) -> APIRouter:
    """
    Create an APIRouter for company jobs endpoints with injected strategy.

    Args:
        jobs_strategy (dict[str, callable]): Mapping of source to strategy factory.

    Returns:
        APIRouter: Configured router with endpoints.
    """
    company_jobs_router = APIRouter()

    @company_jobs_router.post("/get/leads/{type}")
    @mcp_prospectio.tool(
        description="Return companies, jobs, contacts from the database." \
        "The first parameter is the type of data to retrieve, it can be companies, jobs, contacts or leads.",
    )
    async def get_leads(type: str = Path(..., description="Lead source")) -> Union[Leads, CompanyEntity, JobEntity, ContactEntity]:
        try:
            leads = await GetLeadsUseCase(type, repository).get_leads()
            return leads
        except Exception as e:
            logger.error(f"Error in get leads: {e}\n{traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))
        
    @company_jobs_router.post("/insert/leads/{source}")
    @mcp_prospectio.tool(
        description="Find leads and insert them in database from the specified source."
        "the first parameter is the source, it can be mantiks, jsearch, active_jobs_db or mock."
        "The second parameter is the location country code, and the third parameter is a list of job titles." \
        "For job titles prefer using technologies names like : Developer Python, Developer AI, Developer FastApi ..." \
        "Before using this endpoint you must know the user profile. Or you can get the profile from database or if nothing is found, you can ask the user for updating the profile" \
    )
    async def insert_leads(
        source: str = Path(..., description="Lead source"),
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
            strategy = jobs_strategy[source](location, job_title)
            leads = await InsertCompanyJobsUseCase(strategy, repository).insert_leads()
            return leads
        except Exception as e:
            logger.error(f"Error in insert leads: {e}\n{traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

    return company_jobs_router


