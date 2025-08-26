from pydantic import BaseModel

class CompanyInfo(BaseModel):
    """
    Model representing company information for lead enrichment.

    Attributes:
        industry (list[str]): The industry sector of the company.
        compatibility (str): Compatibility score with the lead.
        location (list[str]): The location of the company.
        size (str): Number of employees in the company.
        revenue (str): Annual revenue of the company.
    """
    industry: list[str]
    compatibility: str
    location: list[str]
    size: str
    revenue: str
