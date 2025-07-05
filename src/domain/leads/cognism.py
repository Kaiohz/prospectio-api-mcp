from domain.ports.prospect_api import ProspectAPIPort
from domain.leads.strategy import GetLeadsStrategy


class CognismStrategy(GetLeadsStrategy):
    """
    Strategy for retrieving leads with contacts from Cognism.
    Implements the GetLeadsStrategy interface for the Cognism provider.
    """
    def __init__(self, location: str, job_title: list[str], port: ProspectAPIPort):
        """
        Initialize the CognismStrategy.

        Args:
            location (str): The location to search for leads.
            job_title (list[str]): List of job titles to filter leads.
            port (ProspectAPIPort): The port interface to the external prospect API.
        """
        super().__init__(location, job_title, port)

    async def execute(self) -> dict:
        """
        Execute the strategy to fetch leads from Cognism.

        Returns:
            dict: The leads data retrieved from the external API.
        """
        return await self.port.fetch_leads()
