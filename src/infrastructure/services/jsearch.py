import httpx
from typing import TypeVar
from infrastructure.dto.rapidapi.jsearch import JSearchResponseDTO
from config import JsearchConfig
from infrastructure.api.client import BaseApiClient

T = TypeVar("T")


class JsearchAPI:
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
            "x-rapidapi-key": self.api_key
        }
        self.search_endpoint = "/search"


    async def _check_error(self, client: BaseApiClient,result: httpx.Response, dto_type: type[T]) -> T:
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

    async def fetch_company_jobs(self, location: str, job_title: list[str]) -> dict:
        """
        Fetch jobs from the JSearch API based on search parameters.

        Args:
            query (str): The search query string.
            page (int, optional): The page number. Defaults to 1.
            num_pages (int, optional): Number of pages to fetch. Defaults to 1.
            country (Optional[str], optional): Country code. Defaults to None.
            date_posted (Optional[str], optional): Date posted filter. Defaults to None.
            language (Optional[str], optional): Language filter. Defaults to None.

        Returns:
            JSearchResponseDTO: The DTO containing the job search results.
        """
        params = {
            "query": f"{" ".join(job_title)} in {location}",
            "page": 1,
            "num_pages": 1,
            "date_posted": "month",
            "country": location[0:2].lower()
        }
        client = BaseApiClient(self.api_base, self.headers)
        result = await client.get(self.search_endpoint, params)
        jsearch = await self._check_error(client, result, JSearchResponseDTO)
        return jsearch.model_dump()
