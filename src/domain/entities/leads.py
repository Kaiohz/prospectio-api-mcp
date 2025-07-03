from typing import Any, List
from pydantic import BaseModel, Field

class contact(BaseModel):
    """
    Represents a business contact with name, email, and phone number.
    """
    name: str = Field(..., description="Name of the contact")
    email: str = Field(..., description="Email address of the contact")
    phone: str = Field(..., description="Phone number of the contact")

class company(BaseModel):
    """
    Represents a company with name, industry, size, and location.
    """
    name: str = Field(..., description="Name of the company")
    industry: str = Field(..., description="Industry of the company")
    size: int = Field(..., description="Size of the company in terms of employees")
    location: str = Field(..., description="Location of the company")
    
class Leads(BaseModel):
    """
    Aggregates companies and contacts for lead data.
    """
    companies: List[company] = Field(..., description="List of companies associated with the leads")
    contacts: List[contact] = Field(..., description="List of contacts associated with the leads")
