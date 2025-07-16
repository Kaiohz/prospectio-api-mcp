from typing import Optional
from pydantic import BaseModel, Field


class WorkExperience(BaseModel):
    """Represents a work experience entry in a profile request."""
    
    position: Optional[str] = Field(None, description="Job position or title")
    company: Optional[str] = Field(None, description="Company name")
    start_date: Optional[str] = Field(None, description="Start date in YYYY-MM format")
    end_date: Optional[str] = Field(None, description="End date in YYYY-MM format or 'Present'")
    description: Optional[str] = Field(None, description="Description of the role and responsibilities")
