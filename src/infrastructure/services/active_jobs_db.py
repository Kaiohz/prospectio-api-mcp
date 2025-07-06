import httpx
from typing import TypeVar
from infrastructure.dto.rapidapi.active_jobs_db import ActiveJobsResponseDTO
from config import ActiveJobsDBConfig
from infrastructure.api.client import BaseApiClient

T = TypeVar("T")


class ActiveJobsDBAPI:
    """
    Adapter for the Active Jobs DB API to fetch job data.
    """

    def __init__(self, config: ActiveJobsDBConfig) -> None:
        """
        Initialize ActiveJobsDbAPI with configuration.

        Args:
            config (RapidApiConfig): Active Jobs DB API configuration object.
        """
        self.api_base = config.ACTIVE_JOBS_DB_URL
        self.api_key = config.RAPIDAPI_API_KEY
        self.headers = {
            "accept": "application/json",
            "x-rapidapi-host": self.api_base.split("//")[-1].split("/")[0],
            "x-rapidapi-key": self.api_key
        }
        self.endpoint = "/active-ats-7d"

    async def _check_error(
        self,
        client: BaseApiClient,
        result: httpx.Response,
        dto_type: type[T]
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
            raise Exception(f"Failed to fetch jobs: {result.text}")
        dto = dto_type(result.json())
        await client.close()
        return dto

    async def fetch_company_jobs(self, location: str, job_title: list[str]) -> dict:
        """
        Fetch active jobs from the Active Jobs DB API with advanced filters.

        Args:
            limit (int): Number of jobs to return.
            offset (int): Offset for pagination.
            advanced_title_filter (str): Advanced title filter string.
            location_filter (str): Location filter string.
            description_type (str): Description type.

        Returns:
            dict: A dictionary containing the job search results.
        """
        params = {
            "limit": 10,
            "offset": 0,
            "advanced_title_filter": f"{" | ".join(job_title)}",
            "location_filter": location,
            "description_type": "text"
        }
        client = BaseApiClient(self.api_base, self.headers)
        result = await client.get(self.endpoint, params)
        active_jobs = await self._check_error(client, result, ActiveJobsResponseDTO)
        return {"active_jobs": active_jobs}