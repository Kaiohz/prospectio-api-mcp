from typing import List, Optional
from pydantic import BaseModel, Field

from .work_experience import WorkExperience


class Profile(BaseModel):
    """Represents a user profile with personal and professional information."""
    
    job_title: Optional[str] = Field(None, description="Current job title")
    location: Optional[str] = Field(None, description="Current location")
    bio: Optional[str] = Field(None, description="Professional biography")
    work_experience: List[WorkExperience] = Field(
        default_factory=list, 
        description="List of work experiences"
    )
