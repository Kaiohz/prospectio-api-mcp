from abc import ABC, abstractmethod
from domain.ports.prospect_api import ProspectAPIPort


class GetLeadsStrategy(ABC):
    """
    Abstract base class (strategy) for getting leads with contacts from a data provider.
    """
    def __init__(self, location: str, job_title: list[str], port: ProspectAPIPort):
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