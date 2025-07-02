import httpx
from application.ports.prospect_api import ProspectAPIPort
from domain.dto.mantiks.company import CompanyResponseDTO
from domain.dto.mantiks.location import LocationResponseDTO
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
        if result.status_code != 200:
            await client.close()
            raise Exception(f"Failed to fetch leads: {result.text}")
        if result.status_code == 200:
            dto = dto_type(**result.json())
            await client.close()
            return dto.model_dump()


    async def _get_locations(self, location: str) -> LocationResponseDTO:
        """
        Fetch locations from the Mantiks API.
        """
        mantiks_client = BaseApiClient(self.api_base, self.headers)
        result = await mantiks_client.get(self.locations_endpoint, {"name": location})
        return await self._check_error(mantiks_client, result, LocationResponseDTO)
    
    async def fetch_leads(self, location: str) -> dict:
        """
        Fetch leads from the Mantiks API.
        Returns a mock JSON with companies and contacts.
        """
        locations = await self._get_locations(location)
        locations_ids = [location.id for location in locations.results if location.type == "country"]
        mantiks_client = BaseApiClient(self.api_base, self.headers)
        result = await mantiks_client.get(self.companys_endpoint, {"job_age_in_days": 30, "job_location_ids": locations_ids})
        return await self._check_error(mantiks_client, result, CompanyResponseDTO)