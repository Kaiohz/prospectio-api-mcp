import httpx
from domain.entities import leads
from domain.entities.company import Company, CompanyEntity
from domain.entities.contact import Contact, ContactEntity
from domain.entities.leads import Leads
from domain.entities.job import JobEntity, Job
from prospectio_api_mcp.domain.ports.fetch_leads import FetchLeadsPort
from infrastructure.dto.mantiks.company_response import CompanyResponseDTO
from infrastructure.dto.mantiks.location import LocationResponseDTO
from config import MantiksConfig
from infrastructure.api.client import BaseApiClient
from typing import TypeVar
from datetime import datetime

T = TypeVar("T")


class MantiksAPI(FetchLeadsPort):
    """
    Adapter for the Mantiks API to fetch lead and location data.
    """

    def __init__(self, config: MantiksConfig) -> None:
        """
        Initialize MantiksAPI with configuration.

        Args:
            config (MantiksConfig): Mantiks API configuration object.
        """
        self.api_base = config.MANTIKS_API_URL
        self.api_key = config.MANTIKS_API_KEY
        self.headers = {"accept": "application/json", "x-api-key": self.api_key}
        self.locations_endpoint = "/location/search"
        self.companys_endpoint = "/company/search"

    async def to_company_entity(self, dto: CompanyResponseDTO) -> CompanyEntity:
        """
        Maps a CompanyDTO object from the infrastructure layer to a Company entity in the domain layer.

        Args:
            dto (CompanyDTO): The data transfer object to map.

        Returns:
            Company: The mapped Company entity.
        """
        companies: list[Company] = []
        for mantiks_company in dto.companies if dto.companies else []:
            company = Company(  # type: ignore
                id=mantiks_company.id,
                name=mantiks_company.name,
                source="mantiks",
                size=f"{mantiks_company.min_company_size} - {mantiks_company.max_company_size}",
                website=mantiks_company.website,
            )
            companies.append(company)
        return CompanyEntity(companies)

    async def to_job_entity(self, dto: CompanyResponseDTO) -> JobEntity:
        jobs: list[Job] = []
        for company in dto.companies if dto.companies else []:
            for job in company.jobs if company.jobs else []:
                job_entity = Job(
                    id=job.job_id,
                    company_id=company.id,
                    date_creation=job.date_creation or datetime.now().isoformat(),
                    description=job.description,
                    job_title=job.job_title,
                    location=job.location,
                    salary=(
                        f"{job.salary.min} - {job.salary.max}" if job.salary else None
                    ),
                    job_seniority=job.job_seniority,
                    job_type=job.job_type,
                    sectors=" ".join(job.sectors) if job.sectors else None,
                    apply_url=[
                        job.indeed_apply_url or "",
                        job.linkedin_apply_url or "",
                    ],
                )
                jobs.append(job_entity)
        return JobEntity(jobs)

    async def to_contact_entity(self, dto: CompanyResponseDTO) -> ContactEntity:
        contacts: list[Contact] = []
        for company in dto.companies if dto.companies else []:
            for job in company.jobs if company.jobs else []:
                contact_entity = Contact(  # type: ignore
                    company_id=company.id,
                    job_id=job.job_id,
                    name=job.linkedin_recruiter_name or None,
                    title=job.linkedin_recruiter_title or None,
                    profile_url=job.linkedin_recruiter_link or None,
                )
                contacts.append(contact_entity)
        return ContactEntity(contacts)

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

    async def _get_locations(self, location: str) -> LocationResponseDTO:
        """
        Fetch locations from the Mantiks API for a given location name.

        Args:
            location (str): The name of the location to search for.

        Returns:
            LocationResponseDTO: The DTO containing the location search results.
        """
        mantiks_client = BaseApiClient(self.api_base, self.headers)
        result = await mantiks_client.get(self.locations_endpoint, {"name": location})
        locations = await self._check_error(mantiks_client, result, LocationResponseDTO)
        return locations

    async def fetch_leads(self, location: str, job_title: list[str]) -> Leads:
        """
        Fetch leads from the Mantiks API based on location and job titles.

        Args:
            location (str): The location to search for leads.
            job_title (list[str]): List of job titles to filter leads.

        Returns:
            dict: A dictionary containing companies and contacts data.
        """
        locations = await self._get_locations(location)
        locations_ids = [
            location.id for location in locations.results if location.type == "country"
        ]
        mantiks_client = BaseApiClient(self.api_base, self.headers)
        params = {
            "job_age_in_days": 30,
            "job_location_ids": locations_ids,
            "job_title": job_title,
        }
        result = await mantiks_client.get(self.companys_endpoint, params)
        companies = await self._check_error(mantiks_client, result, CompanyResponseDTO)

        company_entity = await self.to_company_entity(companies)
        job_entity = await self.to_job_entity(companies)
        contact_entity = await self.to_contact_entity(companies)

        leads = Leads(
            companies=company_entity, jobs=job_entity, contacts=contact_entity
        )
        return leads
