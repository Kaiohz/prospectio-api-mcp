from pydantic import BaseModel, Field

class ContactInfo(BaseModel):
    """
    Represents a business contact with optional fields: name, email, phone, and company name.
    """
    name: str
    email: list[str]
    title: str
    phone: str
    profile_url: list[str]