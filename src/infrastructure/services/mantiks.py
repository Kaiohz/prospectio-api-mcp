import httpx
from domain.ports.prospect_api import ProspectAPIPort
from application.dto.mantiks.company import CompanyResponseDTO
from application.dto.mantiks.location import LocationResponseDTO
from config import MantiksConfig
from infrastructure.api.client import BaseApiClient
from typing import TypeVar


T = TypeVar("T")

class MantiksAPI(ProspectAPIPort):

    def __init__(self, config: MantiksConfig) -> None:
        """
        Initialize MantiksAPI with configuration.
        """
        self.api_base = config.MANTIKS_API_BASE
        self.api_key = config.MANTIKS_API_KEY
        self.headers = {
            "accept": "application/json",
            "x-api-key": config.MANTIKS_API_KEY
        }
        self.locations_endpoint = "/location/search"
        self.companys_endpoint = "/company/search"

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
        if result.status_code == 200:
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
    
    async def fetch_leads(self, location: str, job_title: list[str]) -> dict:
        """
        Fetch leads from the Mantiks API based on location and job titles.

        Args:
            location (str): The location to search for leads.
            job_title (list[str]): List of job titles to filter leads.

        Returns:
            dict: A dictionary containing companies and contacts data.
        """
        locations = await self._get_locations(location)
        locations_ids = [location.id for location in locations.results if location.type == "country"]
        mantiks_client = BaseApiClient(self.api_base, self.headers)
        result = await mantiks_client.get(self.companys_endpoint, {"job_age_in_days": 30, "job_location_ids": locations_ids, "job_title": job_title})
        companies = await self._check_error(mantiks_client, result, CompanyResponseDTO)
        return companies.model_dump()