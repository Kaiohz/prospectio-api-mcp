from typing import List, Optional
from pydantic import BaseModel, Field, RootModel

class Job(BaseModel):
    """
    Represents a company with optional fields to match frontend requirements.
    """

    id: Optional[str] = Field(None, description="Unique identifier for the company")
    company_id: Optional[str] = Field(
        None, description="ID of the company associated with the job"
    )
    date_creation: Optional[str] = Field(
        None, description="Creation date of the job posting"
    )
    description: Optional[str] = Field(None, description="Description of the job")
    job_title: Optional[str] = Field(None, description="Title of the job")
    location: Optional[str] = Field(None, description="Location of the job")
    salary: Optional[str] = Field(None, description="Salary details for the job")
    job_seniority: Optional[str] = Field(
        None, description="Seniority level of the job (e.g., junior, mid, senior)"
    )
    job_type: Optional[str] = Field(
        None, description="Type of job (e.g., full-time, part-time)"
    )
    sectors: Optional[str] = Field(
        None, description="List of sectors related to the job"
    )
    apply_url: Optional[list[str]] = Field(
        None, description="List of URLs to apply for the job"
    )


class JobEntity(RootModel[List[Job]]):
    """
    DTO for a list of active jobs.
    """

    pass
