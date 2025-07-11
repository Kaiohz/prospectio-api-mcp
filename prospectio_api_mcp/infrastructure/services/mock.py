from domain.ports.company_jobs import CompanyJobsPort
from config import MockConfig
from prospectio_api_mcp.domain.entities.leads import Leads


class MockAPI(CompanyJobsPort):
    """
    Adapter for the Mantiks API to fetch lead and location data.
    """

    def __init__(self, config: MockConfig) -> None:
        """
        Initialize MantiksAPI with configuration.

        Args:
            config (MantiksConfig): Mantiks API configuration object.
        """
        self.api_base = config.MOCK_API_URL
        self.api_key = config.MOCK_API_KEY
        self.headers = {"accept": "application/json", "x-api-key": self.api_key}
        self.locations_endpoint = "/location/search"
        self.companys_endpoint = "/company/search"

    async def fetch_company_jobs(self, location: str, job_title: list[str]) -> Leads:
        """
        Fetch leads from the Mantiks API based on location and job titles.

        Args:
            location (str): The location to search for leads.
            job_title (list[str]): List of job titles to filter leads.

        Returns:
            dict: A dictionary containing companies and contacts data.
        """
        return Leads(companies=None, jobs=None,contacts=None)
        return {
            "leads": [
                {
                    "company": "Acme Corp",
                    "location": location,
                    "job_title": job_title[0] if job_title else "Unknown",
                    "contact": {"name": "John Doe", "email": "john.doe@acme.com"},
                }
            ]
        }
