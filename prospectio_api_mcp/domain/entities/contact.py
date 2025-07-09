from typing import Optional, List
from pydantic import BaseModel, Field, RootModel


class Contact(BaseModel):
    """
    Represents a business contact with optional fields: name, email, phone, and company name.
    """

    company_id: Optional[str] = Field(
        None, description="Name of the company associated with the contact"
    )
    job_id: Optional[str] = Field(None, description="ID of the job associated with the contact")
    name: Optional[str] = Field(None, description="Name of the contact")
    email: Optional[str] = Field(None, description="Email address of the contact")
    title: Optional[str] = Field(None, description="Title of the contact")
    phone: Optional[str] = Field(None, description="Phone number of the contact")
    profile_url: Optional[str] = Field(
        None, description="URL to the contact's profile (e.g., LinkedIn)"
    )

class ContactEntity(RootModel[List[Contact]]):
    """
    DTO for a list of contacts.
    """
    pass
