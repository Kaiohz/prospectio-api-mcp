from abc import ABC, abstractmethod
from domain.ports.company_jobs import CompanyJobsPort


class CompanyJobsStrategy(ABC):
    """
    Abstract base class (strategy) for getting leads with contacts from a data provider.
    """
    def __init__(self, location: str, job_title: list[str], port: CompanyJobsPort):
        """
        Initialize the strategy with location, job titles, and the port to the provider.

        Args:
            location (str): The location to search for leads.
            job_title (list[str]): List of job titles to filter leads.
            port (ProspectAPIPort): The port interface to the external prospect API.
        """
        self.location = location
        self.port = port
        self.job_title = job_title

    @abstractmethod
    async def execute(self) -> dict:
        """
        Execute the strategy to fetch leads from the provider.

        Returns:
            dict: The leads data retrieved from the external API.
        """
        pass
