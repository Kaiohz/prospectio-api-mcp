from abc import ABC, abstractmethod
from domain.ports.company_jobs import CompanyJobsPort
from prospectio_api_mcp.domain.entities.leads import Leads


class CompanyJobsStrategy(ABC):
    """
    Abstract base class for company jobs lead retrieval strategies.

    This strategy defines the contract for fetching leads with contacts from a data provider.
    It should be extended by concrete implementations for each provider.
    """

    def __init__(self, location: str, job_title: list[str], port: CompanyJobsPort):
        """
        Initialize the strategy with location, job titles, and the provider port.

        Args:
            location (str): The location to search for leads.
            job_title (list[str]): List of job titles to filter leads.
            port (CompanyJobsPort): The port interface to the external company jobs provider.
        """
        self.location = location
        self.port = port
        self.job_title = job_title

    @abstractmethod
    async def execute(self) -> Leads:
        """
        Execute the strategy to fetch leads from the provider.

        Returns:
            dict: The leads data retrieved from the external provider API.
        """
        pass
