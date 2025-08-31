from typing import Optional
from pydantic import BaseModel, Field

from domain.entities.company import CompanyEntity
from domain.entities.contact import ContactEntity
from domain.entities.job import JobEntity


class Leads(BaseModel):
    """
    Represents a business contact with optional fields: name, email, phone, and company name.
    """

    companies: Optional[CompanyEntity] = Field(None, description="List of companies")
    jobs: Optional[JobEntity] = Field(
        None, description="List of jobs associated with the companies"
    )
    contacts: Optional[ContactEntity] = Field(
        None, description="List of contacts associated with the companies and jobs"
    )
    pages: Optional[int] = Field(None, description="Total number of pages available")
