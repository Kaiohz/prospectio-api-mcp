from typing import Optional, List
from pydantic import BaseModel, Field, RootModel


class LeadsResult(BaseModel):
    """
    Represents the result of a leads retrieval operation.
    Contains lists of companies, jobs, and contacts.
    """

    companies: str = Field("", description="Number of companies retrieved")
    jobs: str = Field("", description="Number of jobs retrieved")
    contacts: str = Field("", description="Number of contacts retrieved")
