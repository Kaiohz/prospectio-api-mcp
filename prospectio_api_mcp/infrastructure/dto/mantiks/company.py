from typing import List, Dict, Optional
from pydantic import BaseModel
from infrastructure.dto.mantiks.job import JobDTO

class CompanyDTO(BaseModel):
    """
    Data Transfer Object representing a company and its job offers.

    Attributes:
        id (Optional[str]): Unique identifier for the company.
        jobs (Optional[List[JobDTO]]): List of job offers at the company.
        max_company_size (Optional[int]): Maximum size of the company.
        min_company_size (Optional[int]): Minimum size of the company.
        name (Optional[str]): Name of the company.
        social_urls (Optional[Dict[str, str]]): Social media URLs for the company.
        website (Optional[str]): Website of the company.
    """

    id: Optional[str] = None
    jobs: Optional[List[JobDTO]] = None
    max_company_size: Optional[int] = None
    min_company_size: Optional[int] = None
    name: Optional[str] = None
    social_urls: Optional[Dict[str, str]] = None
    website: Optional[str] = None
