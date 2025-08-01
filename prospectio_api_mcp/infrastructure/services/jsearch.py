from uuid import uuid4
import httpx
from typing import TypeVar
from prospectio_api_mcp.domain.ports.fetch_leads import FetchLeadsPort
from infrastructure.dto.rapidapi.jsearch import JSearchResponseDTO
from config import JsearchConfig
from infrastructure.api.client import BaseApiClient
from domain.entities.company import Company, CompanyEntity
from domain.entities.job import Job, JobEntity
from prospectio_api_mcp.domain.entities.leads import Leads
from datetime import datetime
import asyncio


T = TypeVar("T")


class JsearchAPI(FetchLeadsPort):
    """
    Adapter for the JSearch API to fetch job data.
    """

    def __init__(self, config: JsearchConfig) -> None:
        """
        Initialize JSearchAPI with configuration.

        Args:
            config (JSearchConfig): JSearch API configuration object.
        """
        self.api_base = config.JSEARCH_API_URL
        self.api_key = config.RAPIDAPI_API_KEY
        self.headers = {
            "accept": "application/json",
            "x-rapidapi-host": self.api_base.split("//")[-1].split("/")[0],
            "x-rapidapi-key": self.api_key,
        }
        self.search_endpoint = "/search"

    async def _check_error(
        self, client: BaseApiClient, result: httpx.Response, dto_type: type[T]
    ) -> T:
        """
        Check the HTTP response for errors and parse the response into the given DTO type.
        Closes the client after processing.

        Args:
            client (BaseApiClient): The API client instance to close.
            result (httpx.Response): The HTTP response from the API call.
            dto_type (type[T]): The DTO class to parse the response into.

        Raises:
            Exception: If the response status code is not 200.

        Returns:
            T: An instance of the DTO type with the response data.
        """
        if result.status_code != 200:
            await client.close()
            raise Exception(f"Failed to fetch leads: {result.text}")
        dto = dto_type(**result.json())
        await client.close()
        return dto

    async def to_company_entity(
        self, dto: JSearchResponseDTO
    ) -> tuple[CompanyEntity, list[str]]:
        """
        Convert JSearch response DTO to CompanyEntity.

        Args:
            dto (JSearchResponseDTO): The JSearch API response data.

        Returns:
            CompanyEntity: Entity containing companies from JSearch data.
        """
        companies: list[Company] = []
        ids: list[str] = []
        for jsearch_company in dto.data if dto.data else []:
            company = Company(  # type: ignore
                id=str(uuid4()), name=jsearch_company.employer_name, source="jsearch"
            )
            ids.append(company.id or str(uuid4()))
            companies.append(company)
        return CompanyEntity(companies), ids

    async def to_job_entity(self, dto: JSearchResponseDTO, ids: list[str]) -> JobEntity:
        """
        Convert JSearch response DTO to JobEntity.

        Args:
            dto (JSearchResponseDTO): The JSearch API response data.

        Returns:
            JobEntity: Entity containing jobs from JSearch data.
        """
        jobs: list[Job] = []
        for index, job in enumerate(dto.data) if dto.data else []:
            job.job_id = str(uuid4())
            job_entity = Job(  # type: ignore
                id=job.job_id,
                company_id=ids[index],
                date_creation=(
                    job.job_posted_at_datetime_utc.rstrip("Z")
                    if job.job_posted_at_datetime_utc
                    else datetime.now().isoformat()
                ),
                description=job.job_description,
                job_title=job.job_title,
                location=job.job_location,
                salary=f"{job.job_min_salary or ''} - {job.job_max_salary or ''}",
                job_type=job.job_employment_type,
                apply_url=[job.job_apply_link or "", job.job_google_link or ""],
            )
            jobs.append(job_entity)
        return JobEntity(jobs)

    async def process_results(
        self, company_result: CompanyEntity, job_result: JobEntity, params: dict
    ) -> None:
        await asyncio.sleep(1)  # Rate limiting to avoid hitting API limits
        client = BaseApiClient(self.api_base, self.headers)
        result = await client.get(self.search_endpoint, params)
        jsearch = await self._check_error(client, result, JSearchResponseDTO)
        company_entity, ids = await self.to_company_entity(jsearch)
        job_entity = await self.to_job_entity(jsearch, ids)
        company_result.root.extend(company_entity.root)
        job_result.root.extend(job_entity.root)

    async def fetch_leads(self, location: str, job_title: list[str]) -> Leads:
        """
        Fetch jobs from the JSearch API based on search parameters.

        Args:
            location (str): The location to search jobs in.
            job_title (list[str]): List of job titles to search for.

        Returns:
            Leads: The leads containing companies and jobs data.
        """
        params_list = []
        company_result: CompanyEntity = CompanyEntity([])
        job_result: JobEntity = JobEntity([])

        for title in job_title[:2]:
            params = {
                "query": f"{title} in {location}",
                "page": 1,
                "num_pages": 1,
                "date_posted": "month",
                "country": location[0:2].lower(),
            }
            params_list.append(params)

        await asyncio.gather(
            *[
                self.process_results(company_result, job_result, params)
                for params in params_list
            ]
        )

        # Combine results into a Leads object
        leads = Leads(
            companies=company_result,
            jobs=job_result,
            contacts=None,
        )
        return leads
