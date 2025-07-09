from typing import List, Optional
from pydantic import BaseModel


class LocationResultDTO(BaseModel):
    """
    Data Transfer Object representing a location result (country, region, city).

    Attributes:
        country (Optional[str]): The country name, if available.
        full_name (str): The full name of the location.
        id (int): Unique identifier for the location.
        name (str): The short name of the location.
        type (str): The type of location (e.g., country, region, city).
    """

    country: Optional[str]
    full_name: str
    id: int
    name: str
    type: str


class LocationResponseDTO(BaseModel):
    """
    Data Transfer Object representing the complete response for a location search.

    Attributes:
        nb_results (int): Number of results found.
        results (List[LocationResultDTO]): List of location results.
    """

    nb_results: int
    results: List[LocationResultDTO]
