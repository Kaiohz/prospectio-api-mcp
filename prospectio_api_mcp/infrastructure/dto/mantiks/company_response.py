from typing import Optional, List
from pydantic import BaseModel

from infrastructure.dto.mantiks.company import CompanyDTO


class CompanyResponseDTO(BaseModel):
    """
    Data Transfer Object representing the complete response for a company and job search.

    Attributes:
        companies (Optional[List[CompanyDTO]]): List of companies found.
        credits_cost (Optional[int]): Number of credits used for the search.
        credits_remaining (Optional[int]): Number of credits remaining.
        nb_companies (Optional[int]): Number of companies found.
        nb_jobs (Optional[int]): Number of jobs found.
    """

    companies: Optional[List[CompanyDTO]] = None
    credits_cost: Optional[int] = None
    credits_remaining: Optional[int] = None
    nb_companies: Optional[int] = None
    nb_jobs: Optional[int] = None
