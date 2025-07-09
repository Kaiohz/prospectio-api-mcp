import httpx
from typing import TypeVar
from domain.ports.company_jobs import CompanyJobsPort
from infrastructure.dto.rapidapi.active_jobs_db import ActiveJobsResponseDTO
from config import ActiveJobsDBConfig
from infrastructure.api.client import BaseApiClient

T = TypeVar("T")


class ActiveJobsDBAPI(CompanyJobsPort):
    """
    Adapter for the Active Jobs DB API. Handles fetching job data from the external Active Jobs DB service.
    """

    def __init__(self, config: ActiveJobsDBConfig) -> None:
        """
        Initialize the ActiveJobsDBAPI adapter with the given configuration.

        Args:
            config (ActiveJobsDBConfig): Configuration object for the Active Jobs DB API.

        Returns:
            None
        """
        self.api_base = config.ACTIVE_JOBS_DB_URL
        self.api_key = config.RAPIDAPI_API_KEY
        self.headers = {
            "accept": "application/json",
            "x-rapidapi-host": self.api_base.split("//")[-1].split("/")[0],
            "x-rapidapi-key": self.api_key,
        }
        self.endpoint = "/active-ats-7d"

    async def _check_error(
        self, client: BaseApiClient, result: httpx.Response, dto_type: type[T]
    ) -> T:
        """
        Check the HTTP response for errors and parse the response into the given DTO type. Always closes the client.

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
            raise Exception(f"Failed to fetch jobs: {result.text}")
        dto = dto_type(**{"active_jobs": result.json()})
        await client.close()
        return dto

    async def fetch_company_jobs(self, location: str, job_title: list[str]) -> dict:
        """
        Fetch active jobs from the Active Jobs DB API using advanced filters.

        Args:
            location (str): The location filter for the job search.
            job_title (list[str]): List of job titles to filter by.

        Returns:
            dict: Dictionary containing the job search results under the key 'active_jobs'.
        """
        params = {
            "limit": 10,
            "offset": 0,
            "advanced_title_filter": f"{" | ".join(job_title)}",
            "location_filter": location,
            "description_type": "text",
        }
        client = BaseApiClient(self.api_base, self.headers)
        result = await client.get(self.endpoint, params)
        active_jobs = await self._check_error(client, result, ActiveJobsResponseDTO)
        return {"active_jobs": active_jobs.model_dump()}
