from abc import ABC, abstractmethod
from domain.entities.leads import Leads


class CompanyJobsPort(ABC):
    """
    Abstract port interface for fetching leads from an external provider.
    """

    @abstractmethod
    async def fetch_company_jobs(self, location: str, job_title: list[str]) -> Leads:
        """
        Fetch leads from the provider.

        Args:
            location (str): The location to search for leads.
            job_title (list[str]): List of job titles to filter leads.
        Returns:
            dict: The leads data retrieved from the provider.
        """
        pass
