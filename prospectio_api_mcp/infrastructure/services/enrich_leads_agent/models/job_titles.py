from pydantic import BaseModel, Field

from domain.entities import job

class JobTitles(BaseModel):
    """
    Represents a business contact with optional fields: name, email, phone, and company name.
    """
    job_titles: list[str]