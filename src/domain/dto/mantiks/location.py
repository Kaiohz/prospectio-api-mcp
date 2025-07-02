from typing import List, Optional
from pydantic import BaseModel

class LocationResultDTO(BaseModel):
    """DTO représentant un résultat de localisation (pays, région, ville)."""
    country: Optional[str]
    full_name: str
    id: int
    name: str
    type: str

class LocationResponseDTO(BaseModel):
    """DTO représentant la réponse complète de recherche de localisation."""
    nb_results: int
    results: List[LocationResultDTO]
